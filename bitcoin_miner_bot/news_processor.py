"""
News Processor Module

Handles fetching and processing of Bitcoin mining news from various sources:
- Event Registry API for mining-related news
- RSS feeds from mining-focused publications
- Web scraping for article content extraction
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from eventregistry import EventRegistry, QueryArticlesIter

logger = logging.getLogger(__name__)


class NewsProcessor:
    """Process and fetch Bitcoin mining news from multiple sources."""
    
    def __init__(self):
        """Initialize the news processor."""
        self.event_registry_key = os.getenv('EVENT_REGISTRY_API_KEY')
        
        # Keywords for Bitcoin mining news
        self.mining_keywords = [
            "bitcoin mining",
            "cryptocurrency mining",
            "bitcoin miner",
            "mining hardware",
            "ASIC miner",
            "mining pool",
            "hashrate",
            "mining difficulty",
            "bitcoin halving mining"
        ]
        
        # Known Bitcoin mining news sources (domains)
        self.preferred_sources = [
            "coindesk.com",
            "cointelegraph.com",
            "decrypt.co",
            "theblock.co",
            "bitcoinmagazine.com",
            "mining.com",
            "hashrateindex.com"
        ]
        
        logger.info("NewsProcessor initialized")
    
    def fetch_articles(self, max_articles=20):
        """
        Fetch recent Bitcoin mining articles.
        
        Args:
            max_articles: Maximum number of articles to fetch
            
        Returns:
            List of article dictionaries
        """
        logger.info(f"Fetching up to {max_articles} articles")
        articles = []
        
        # Fetch from Event Registry if API key is available
        if self.event_registry_key:
            try:
                articles.extend(self._fetch_from_event_registry(max_articles))
            except Exception as e:
                logger.error(f"Error fetching from Event Registry: {e}", exc_info=True)
        
        # If no Event Registry key or no articles, use fallback sources
        if not articles:
            logger.info("Using fallback RSS/scraping methods")
            articles.extend(self._fetch_from_fallback_sources(max_articles))
        
        # Enhance articles with full content
        for article in articles:
            try:
                self._extract_article_content(article)
            except Exception as e:
                logger.warning(f"Could not extract content for {article.get('url')}: {e}")
        
        logger.info(f"Fetched {len(articles)} articles total")
        return articles[:max_articles]
    
    def _fetch_from_event_registry(self, max_articles):
        """Fetch articles from Event Registry API."""
        logger.info("Fetching from Event Registry")
        articles = []
        
        try:
            er = EventRegistry(apiKey=self.event_registry_key)
            
            # Query for Bitcoin mining articles from the last 24 hours
            query = QueryArticlesIter(
                keywords=" OR ".join(self.mining_keywords),
                lang="eng",
                dateStart=(datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                dateEnd=datetime.now().strftime("%Y-%m-%d")
            )
            
            for article in query.execQuery(er, maxItems=max_articles):
                articles.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('title', ''),
                    'published_date': article.get('dateTime', ''),
                    'body': article.get('body', ''),
                    'image': article.get('image', ''),
                    'fetched_at': datetime.now().isoformat()
                })
            
            logger.info(f"Fetched {len(articles)} articles from Event Registry")
            
        except Exception as e:
            logger.error(f"Event Registry fetch error: {e}", exc_info=True)
        
        return articles
    
    def _fetch_from_fallback_sources(self, max_articles):
        """Fetch articles using fallback methods (mock data for now)."""
        logger.info("Using fallback sources")
        
        # For a working bot, implement RSS parsing or web scraping here
        # For now, return empty list or mock data
        fallback_articles = []
        
        # Example: You could parse RSS feeds like:
        # - https://bitcoinmagazine.com/feed
        # - https://cointelegraph.com/rss
        
        logger.info(f"Fetched {len(fallback_articles)} articles from fallback sources")
        return fallback_articles
    
    def _extract_article_content(self, article):
        """
        Extract full article content using web scraping.
        
        Args:
            article: Article dictionary to enhance with content
        """
        url = article.get('url')
        if not url:
            return
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'aside']):
                element.decompose()
            
            # Try to find article content
            article_body = None
            
            # Common article content selectors
            selectors = [
                'article',
                '.article-content',
                '.post-content',
                '.entry-content',
                '.content',
                'main'
            ]
            
            for selector in selectors:
                article_body = soup.select_one(selector)
                if article_body:
                    break
            
            if article_body:
                # Extract text, preserving paragraphs
                paragraphs = article_body.find_all('p')
                content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
                if content:
                    article['body'] = content[:5000]  # Limit to 5000 chars
                    article['extracted_content'] = True
                    logger.debug(f"Extracted content for: {article.get('title', 'Unknown')}")
            
            # Try to extract image if not present
            if not article.get('image'):
                og_image = soup.find('meta', property='og:image')
                if og_image and og_image.get('content'):
                    article['image'] = og_image['content']
            
        except Exception as e:
            logger.warning(f"Content extraction failed for {url}: {e}")
            article['extracted_content'] = False
    
    def filter_mining_relevant(self, articles):
        """
        Filter articles to ensure they're mining-relevant.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Filtered list of mining-relevant articles
        """
        filtered = []
        
        mining_terms = [
            'mining', 'miner', 'hashrate', 'asic', 'mining pool',
            'mining difficulty', 'mining farm', 'bitcoin mining'
        ]
        
        for article in articles:
            title = article.get('title', '').lower()
            body = article.get('body', '').lower()
            
            # Check if any mining term is in title or body
            if any(term in title or term in body for term in mining_terms):
                filtered.append(article)
                logger.debug(f"Article passed mining filter: {article.get('title', 'Unknown')}")
            else:
                logger.debug(f"Article filtered out: {article.get('title', 'Unknown')}")
        
        logger.info(f"Filtered {len(filtered)} mining-relevant articles from {len(articles)}")
        return filtered
