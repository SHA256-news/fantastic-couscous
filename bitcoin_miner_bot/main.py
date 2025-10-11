# main.py
import os
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import bot modules
from bitcoin_miner_bot import news_processor
from bitcoin_miner_bot import gemini_interface
from bitcoin_miner_bot import twitter_publisher
from bitcoin_miner_bot import image_manager
from bitcoin_miner_bot import github_manager

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

# Repository name for GitHub operations
REPO_NAME = os.getenv("GITHUB_REPOSITORY", "SHA256-news/fantastic-couscous")


def initialize_bot():
    """
    Initializes the bot by loading state and ensuring required files exist.
    """
    logging.info("=== Initializing Bitcoin Mining News Aggregator Bot ===")
    
    # Ensure placeholder images exist
    image_manager.ensure_placeholder_images()
    
    # Load bot state
    state = github_manager.load_bot_state()
    
    # Restore state to news_processor globals
    news_processor.PROCESSED_URLS = set(state.get('processed_urls', []))
    news_processor.PROCESSED_EVENT_URIS = set(state.get('processed_event_uris', []))
    news_processor.DAILY_BRIEF_URLS = set(state.get('daily_brief_urls', []))
    news_processor.LIFO_QUEUE = state.get('lifo_queue', [])
    
    logging.info(f"Loaded state: {len(news_processor.PROCESSED_URLS)} processed URLs, "
                 f"{len(news_processor.LIFO_QUEUE)} items in queue")
    
    return state


def save_bot_state_to_file():
    """
    Saves current bot state to file.
    """
    state = {
        'processed_urls': list(news_processor.PROCESSED_URLS),
        'processed_event_uris': list(news_processor.PROCESSED_EVENT_URIS),
        'daily_brief_urls': list(news_processor.DAILY_BRIEF_URLS),
        'lifo_queue': news_processor.LIFO_QUEUE,
        'last_run': datetime.now().isoformat()
    }
    github_manager.save_bot_state(state)


def process_new_articles(lookback_hours: int = 4):
    """
    Fetches and processes new articles from EventRegistry.
    
    Args:
        lookback_hours: How many hours back to search for articles
    """
    logging.info(f"=== Fetching articles from last {lookback_hours} hours ===")
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=lookback_hours)
    
    # Fetch articles from EventRegistry
    articles = news_processor.get_articles_from_eventregistry(start_time, end_time)
    
    logging.info(f"Processing {len(articles)} candidate articles")
    
    relevant_count = 0
    for article in articles:
        url = article['url']
        er_title = article['er_title']
        er_summary = article['er_summary']
        event_uri = article['event_uri']
        
        logging.info(f"Processing: {er_title}")
        
        # Fetch full article content
        html_title, full_content, article_url_title = news_processor.fetch_article_content(url)
        
        if not full_content:
            logging.warning(f"Skipping {url} - could not fetch content")
            continue
        
        # Semantic filtering with Gemini
        is_relevant = gemini_interface.semantically_filter_article(
            html_title, er_summary, full_content
        )
        
        if is_relevant:
            logging.info(f"✓ Article is relevant: {html_title}")
            relevant_count += 1
            
            # Add to LIFO queue
            news_processor.LIFO_QUEUE.insert(0, {
                'url': url,
                'event_uri': event_uri,
                'html_title': html_title,
                'article_url_title': article_url_title,
                'full_content': full_content,
                'er_title': er_title,
                'er_summary': er_summary,
                'source_title': article.get('source_title', 'Unknown Source')
            })
            
            # Add to daily brief collection
            news_processor.DAILY_BRIEF_URLS.add(url)
        else:
            logging.info(f"✗ Article not relevant: {html_title}")
    
    logging.info(f"Found {relevant_count} relevant articles")
    return relevant_count


def publish_next_tweet():
    """
    Publishes a tweet for the next article in the LIFO queue.
    Returns True if a tweet was published, False otherwise.
    """
    if not news_processor.LIFO_QUEUE:
        logging.info("No articles in queue to tweet")
        return False
    
    # Pop from front of queue (LIFO - most recent first)
    article = news_processor.LIFO_QUEUE.pop(0)
    
    url = article['url']
    html_title = article['html_title']
    article_url_title = article['article_url_title']
    full_content = article['full_content']
    source_title = article['source_title']
    event_uri = article['event_uri']
    
    logging.info(f"=== Preparing tweet for: {html_title} ===")
    
    # Generate tweet content with Gemini
    tweet_content = gemini_interface.generate_tweet_content(
        html_title, full_content, article_url_title
    )
    
    if tweet_content.startswith("ERROR"):
        logging.error(f"Failed to generate tweet content for {url}")
        return False
    
    # Get appropriate images
    image_paths = image_manager.get_image_for_article(
        html_title, full_content, source_title
    )
    
    # Publish tweet
    success, tweet_data = twitter_publisher.publish_tweet(
        tweet_content, url, image_paths
    )
    
    if success:
        logging.info(f"✓ Successfully published tweet: {tweet_data['url']}")
        
        # Mark as processed
        news_processor.PROCESSED_URLS.add(url)
        if event_uri:
            news_processor.PROCESSED_EVENT_URIS.add(event_uri)
        
        # Save state after successful tweet
        save_bot_state_to_file()
        
        return True
    else:
        logging.error(f"✗ Failed to publish tweet for {url}")
        # Re-add to queue for retry
        news_processor.LIFO_QUEUE.insert(0, article)
        return False


def run_tweet_cycle(max_tweets: int = 1):
    """
    Runs a tweet cycle, publishing up to max_tweets.
    
    Args:
        max_tweets: Maximum number of tweets to publish in this cycle
    """
    logging.info(f"=== Running tweet cycle (max {max_tweets} tweets) ===")
    
    tweets_published = 0
    for i in range(max_tweets):
        if publish_next_tweet():
            tweets_published += 1
        else:
            break
    
    logging.info(f"Published {tweets_published} tweets in this cycle")
    return tweets_published


def main():
    """
    Main bot execution function.
    Called by GitHub Actions or can be run locally.
    """
    try:
        # Initialize
        state = initialize_bot()
        
        # Process new articles (last 4 hours)
        process_new_articles(lookback_hours=4)
        
        # Publish tweets (1 per run for regular scheduled execution)
        run_tweet_cycle(max_tweets=1)
        
        # Save final state
        save_bot_state_to_file()
        
        # Push state to GitHub (for persistence across runs)
        github_manager.push_state_to_github(REPO_NAME)
        
        logging.info("=== Bot execution completed successfully ===")
        
    except Exception as e:
        logging.error(f"Bot execution failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
