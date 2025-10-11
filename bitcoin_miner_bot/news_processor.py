# news_processor.py
from eventregistry import EventRegistry, QueryArticles
import os
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timedelta
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ER_API_KEY = os.getenv("EVENT_REGISTRY_API_KEY")
er = EventRegistry(apiKey=ER_API_KEY)

# These globals will be managed by main.py loading/saving bot_state
PROCESSED_URLS = set()  # URLs that have been successfully tweeted
PROCESSED_EVENT_URIS = set()  # EventRegistry URIs that have been successfully tweeted (for story deduplication)
DAILY_BRIEF_URLS = set()  # URLs collected for the current day's brief
LIFO_QUEUE = []  # List of relevant article dicts, ordered LIFO

# Common CSS selectors for robust article content extraction
# This list is ordered by likelihood of containing main article content
ARTICLE_CONTENT_SELECTORS = [
    "article[itemprop='articleBody']",  # Common in many news sites
    "div[itemprop='articleBody']",
    "div.article-content",
    "div.entry-content",
    "div.post-content",
    "div.story-content",
    "div.td-post-content",  # Example from specific themes
    "div.g-article",       # Example from specific themes
    "main article",
    "article main",
    "div.article-body",
    "div.article__content",
    "div#main-content",
    "div#article-content",
    "div#content-main",
    "div#content",  # Generic fallback
    "body"  # Last resort, might pull too much noise
]


def fetch_article_content(url: str) -> tuple[str, str, str]:
    """
    Fetches article content and title from a given URL.
    Returns (html_title, full_content, article_url_title).
    Handles common parsing issues and attempts robust content extraction using lxml and CSS selectors.
    article_url_title is the title that would appear in the URL bar, useful for Gemini's non-repetition constraint.
    """
    try:
        response = requests.get(url, timeout=15)  # Increased timeout slightly for robust fetching
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'lxml')  # Using lxml parser for speed and robustness

        # Get title that would appear in the URL bar (<title> tag)
        title_tag = soup.find('title')
        html_title = title_tag.text.strip() if title_tag else "No Title Found"

        # Get article_url_title for Gemini's prompt (og:title preferred as it's often more curated)
        og_title_meta = soup.find('meta', property='og:title')
        article_url_title = og_title_meta['content'].strip() if og_title_meta else html_title

        full_content = ""
        # Attempt to find content using specific, ordered CSS selectors
        for selector in ARTICLE_CONTENT_SELECTORS:
            content_container = soup.select_one(selector)
            if content_container:
                paragraphs = content_container.find_all('p')
                # Filter out paragraphs that are too short or common boilerplate (e.g., footers, captions)
                filtered_paragraphs = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50 or re.search(r'[a-zA-Z]{5,}', p.get_text())]
                full_content = "\n".join(filtered_paragraphs)
                if full_content.strip():  # If content is found with this selector, break
                    logging.debug(f"Content found using selector: {selector}")
                    break
        
        # Fallback to all paragraphs if specific selectors fail or return insufficient content
        if not full_content.strip():
            logging.debug("No specific selector yielded content, falling back to all paragraphs.")
            paragraphs = soup.find_all('p')
            filtered_paragraphs = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50 or re.search(r'[a-zA-Z]{5,}', p.get_text())]
            full_content = "\n".join(filtered_paragraphs)

        # Basic cleanup: multiple spaces to single space, strip leading/trailing whitespace
        full_content = re.sub(r'\s+', ' ', full_content).strip()

        if not full_content:
            logging.warning(f"Could not extract meaningful content from {url}.")
            # Even if content is empty, return titles to allow Gemini to work with metadata
            return html_title, "", article_url_title

        return html_title, full_content, article_url_title
    except requests.exceptions.RequestException as e:
        logging.warning(f"HTTP or Network error fetching {url}: {e}")
        return "Error Fetching Title", "", "Error Fetching Title"  # Return empty content but error title
    except Exception as e:
        logging.warning(f"Error parsing content from {url}: {e}")
        return "Error Parsing Title", "", "Error Parsing Title"  # Return empty content but error title


def get_articles_from_eventregistry(start_time: datetime, end_time: datetime) -> list[dict]:
    """
    Fetches articles related to Bitcoin mining from EventRegistry within a time range.
    """
    query_start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    query_end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Querying EventRegistry from {query_start_time} to {query_end_time}")

    q = QueryArticles(
        conceptUri=["http://en.wikipedia.org/wiki/Bitcoin_mining"],
        lang="eng",
        dateStart=query_start_time,
        dateEnd=query_end_time,
        sortBy="date",
        sortByAsc=False,  # Most recent first
        maxItems=100  # Fetch a reasonable number to ensure we get relevant ones
    )

    articles_data = []
    try:
        articles = er.execQuery(q)
        if articles and 'articles' in articles and 'results' in articles['articles']:
            for article in articles['articles']['results']:
                url = article.get('url')
                event_uri = article.get('uri')  # EventRegistry's internal event ID for story deduplication

                # Check against processed URLs and event URIs for deduplication
                if url and (url.startswith('http://') or url.startswith('https://')):
                    if url in PROCESSED_URLS:
                        logging.debug(f"Skipping {url} - already processed (URL duplicate).")
                        continue
                    if event_uri and event_uri in PROCESSED_EVENT_URIS:
                        logging.debug(f"Skipping {url} (Event URI: {event_uri}) - already processed (story duplicate).")
                        continue
                    # Check if already in LIFO_QUEUE (already processed and waiting)
                    if any(item['url'] == url for item in LIFO_QUEUE):
                        logging.debug(f"Skipping {url} - already in LIFO queue.")
                        continue
                    
                    articles_data.append({
                        'url': url,
                        'event_uri': event_uri,  # Store EventRegistry URI
                        'er_title': article.get('title', 'No Title'),  # EventRegistry title
                        'er_summary': article.get('body', article.get('snippet', 'No Summary')),  # ER body or snippet
                        'source_title': article.get('source', {}).get('title', 'Unknown Source')
                    })
        logging.info(f"Found {len(articles_data)} new candidate articles from EventRegistry.")
    except Exception as e:
        logging.error(f"Error fetching articles from EventRegistry: {e}")

    return articles_data
