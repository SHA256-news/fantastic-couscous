"""
Bitcoin Mining News Aggregator Bot - Main Entry Point

This module orchestrates the entire bot workflow:
- Fetches Bitcoin mining news
- Processes and enriches content with Gemini AI
- Publishes to Twitter
- Updates GitHub Pages website
- Manages bot state persistence
"""

import os
import sys
import logging
import json
from datetime import datetime
from dotenv import load_dotenv

from news_processor import NewsProcessor
from gemini_interface import GeminiInterface
from twitter_publisher import TwitterPublisher
from image_manager import ImageManager
from github_manager import GitHubManager

# Load environment variables
load_dotenv()

# Configure logging
LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class BitcoinMiningNewsBot:
    """Main bot orchestrator class."""
    
    def __init__(self):
        """Initialize bot components."""
        logger.info("Initializing Bitcoin Mining News Bot")
        
        try:
            self.github_manager = GitHubManager()
            self.news_processor = NewsProcessor()
            self.gemini_interface = GeminiInterface()
            self.twitter_publisher = TwitterPublisher()
            self.image_manager = ImageManager()
            
            # Load bot state
            self.state = self.github_manager.load_state()
            logger.info("Bot initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing bot: {e}", exc_info=True)
            raise
    
    def process_news_queue(self):
        """Process news articles from the queue and publish to Twitter."""
        logger.info("Starting news queue processing")
        
        try:
            # Fetch new articles
            new_articles = self.news_processor.fetch_articles()
            logger.info(f"Fetched {len(new_articles)} new articles")
            
            # Add to queue (LIFO)
            queue = self.state.get('article_queue', [])
            for article in new_articles:
                # Avoid duplicates
                if not any(a.get('url') == article.get('url') for a in queue):
                    queue.insert(0, article)  # LIFO: insert at beginning
                    logger.info(f"Added article to queue: {article.get('title', 'Unknown')}")
            
            self.state['article_queue'] = queue
            
            # Process articles from the top of the queue
            articles_to_process = min(5, len(queue))  # Process up to 5 articles
            logger.info(f"Processing {articles_to_process} articles from queue")
            
            processed_count = 0
            for i in range(articles_to_process):
                if not queue:
                    break
                
                article = queue.pop(0)  # LIFO: take from beginning
                
                try:
                    # Enrich article with Gemini
                    enhanced_article = self.gemini_interface.enhance_article(article)
                    
                    # Select appropriate image
                    image_path = self.image_manager.select_image(enhanced_article)
                    
                    # Generate tweet content
                    tweet_content = self.gemini_interface.generate_tweet_content(enhanced_article)
                    
                    # Publish to Twitter
                    tweet_result = self.twitter_publisher.publish_tweet(
                        content=tweet_content,
                        image_path=image_path,
                        article_url=article.get('url')
                    )
                    
                    if tweet_result:
                        logger.info(f"Successfully published tweet for: {article.get('title', 'Unknown')}")
                        processed_count += 1
                        
                        # Update state with published article
                        published = self.state.get('published_articles', [])
                        published.append({
                            'title': article.get('title'),
                            'url': article.get('url'),
                            'published_at': datetime.now().isoformat(),
                            'tweet_id': tweet_result.get('id')
                        })
                        self.state['published_articles'] = published[-100:]  # Keep last 100
                        
                        # Update GitHub Pages
                        self.github_manager.update_website_tweets(published[-10:])  # Latest 10
                    else:
                        logger.warning(f"Failed to publish tweet, re-adding to queue: {article.get('title', 'Unknown')}")
                        queue.insert(0, article)  # Re-add to front if failed
                        
                except Exception as e:
                    logger.error(f"Error processing article: {e}", exc_info=True)
                    queue.insert(0, article)  # Re-add to front if error
            
            # Update state
            self.state['article_queue'] = queue
            self.state['last_run'] = datetime.now().isoformat()
            self.github_manager.save_state(self.state)
            
            logger.info(f"Queue processing complete. Processed: {processed_count}, Remaining: {len(queue)}")
            return processed_count
            
        except Exception as e:
            logger.error(f"Error in news queue processing: {e}", exc_info=True)
            raise
    
    def run(self):
        """Main bot execution method."""
        logger.info("=== Bot Run Started ===")
        
        try:
            processed = self.process_news_queue()
            logger.info(f"=== Bot Run Complete - Processed {processed} articles ===")
            return processed
            
        except Exception as e:
            logger.error(f"Bot run failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point for the bot."""
    try:
        bot = BitcoinMiningNewsBot()
        bot.run()
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
