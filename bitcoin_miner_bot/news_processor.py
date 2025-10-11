# news_processor.py
import os
import requests
from bs4 import BeautifulSoup
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time

load_dotenv()

# Initialize EventRegistry
er = EventRegistry(apiKey=os.getenv("EVENT_REGISTRY_API_KEY"))

# Keywords for initial filtering (Bitcoin mining-related)
BITCOIN_MINING_KEYWORDS = [
    "bitcoin mining",
    "bitcoin miner",
    "bitcoin miners",
    "ASIC mining",
    "bitcoin hashrate",
    "mining hardware",
    "mining difficulty",
    "mining pool",
    "bitcoin mine",
    "bitcoin farms",
    "mining rig",
    "mining infrastructure"
]

# Known Bitcoin mining companies for additional filtering
MINING_COMPANIES = [
    "Riot Platforms",
    "Marathon Digital",
    "CleanSpark",
    "Bitfarms",
    "Iris Energy",
    "Hive Digital",
    "Core Scientific",
    "Hut 8",
    "Cipher Mining",
    "TeraWulf"
]


def fetch_articles_from_eventregistry(hours_back: int = 2) -> list:
    """
    Fetches articles related to Bitcoin mining from EventRegistry.
    Returns a list of article dictionaries.
    """
    articles = []
    
    # Calculate date range
    date_end = datetime.now()
    date_start = date_end - timedelta(hours=hours_back)
    
    # Build query with Bitcoin mining keywords
    keyword_query = " OR ".join([f'"{kw}"' for kw in BITCOIN_MINING_KEYWORDS])
    company_query = " OR ".join([f'"{company}"' for company in MINING_COMPANIES])
    
    # Combine queries
    full_query = f"({keyword_query}) OR ({company_query})"
    
    try:
        # Query for articles
        q = QueryArticlesIter(
            keywords=full_query,
            dateStart=date_start.strftime("%Y-%m-%d"),
            dateEnd=date_end.strftime("%Y-%m-%d"),
            lang="eng"
        )
        
        # Fetch articles
        for article in q.execQuery(er, sortBy="date", maxItems=50):
            articles.append({
                'id': article.get('uri', ''),
                'title': article.get('title', ''),
                'summary': article.get('body', '')[:500],  # First 500 chars as summary
                'url': article.get('url', ''),
                'date': article.get('dateTime', ''),
                'source': article.get('source', {}).get('title', 'Unknown'),
                'body': article.get('body', '')
            })
            
    except Exception as e:
        print(f"DEBUG: Error fetching articles from EventRegistry: {e}")
    
    return articles


def scrape_article_content(url: str) -> str:
    """
    Scrapes the full article content from a given URL.
    Returns the article text or empty string on failure.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Try to find main content
        content = ""
        
        # Try common article containers
        for selector in ['article', '.article-content', '.post-content', 'main']:
            element = soup.select_one(selector)
            if element:
                content = element.get_text(separator='\n', strip=True)
                break
        
        # Fallback to body if no specific container found
        if not content:
            content = soup.body.get_text(separator='\n', strip=True) if soup.body else ""
        
        return content
        
    except Exception as e:
        print(f"DEBUG: Error scraping article content from {url}: {e}")
        return ""


def process_articles(articles: list, semantic_filter_func) -> list:
    """
    Processes articles by scraping full content and applying semantic filtering.
    Returns a list of relevant article dictionaries.
    """
    relevant_articles = []
    
    for article in articles:
        # Skip if no URL
        if not article.get('url'):
            continue
        
        # Scrape full content
        full_text = scrape_article_content(article['url'])
        
        # Use existing body if scraping fails
        if not full_text:
            full_text = article.get('body', '')
        
        # Apply semantic filtering
        is_relevant = semantic_filter_func(
            article.get('title', ''),
            article.get('summary', ''),
            full_text
        )
        
        if is_relevant:
            article['full_text'] = full_text
            relevant_articles.append(article)
            print(f"DEBUG: Article '{article.get('title', '')}' marked as RELEVANT")
        else:
            print(f"DEBUG: Article '{article.get('title', '')}' marked as NOT RELEVANT")
        
        # Add small delay to avoid rate limiting
        time.sleep(0.5)
    
    return relevant_articles
