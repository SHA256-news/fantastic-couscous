# daily_brief_script.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from bitcoin_miner_bot import github_manager
from bitcoin_miner_bot import daily_brief_generator
from bitcoin_miner_bot import news_processor

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

REPO_NAME = os.getenv("GITHUB_REPOSITORY", "SHA256-news/fantastic-couscous")


def generate_and_publish_brief():
    """
    Generates and publishes the daily brief to GitHub Pages.
    """
    logging.info("=== Generating Daily Brief ===")
    
    # Load bot state to get collected URLs
    state = github_manager.load_bot_state()
    news_processor.PROCESSED_URLS = set(state.get('processed_urls', []))
    news_processor.DAILY_BRIEF_URLS = set(state.get('daily_brief_urls', []))
    
    if not news_processor.DAILY_BRIEF_URLS:
        logging.warning("No articles collected for today's brief")
        return
    
    # Collect article information
    brief_articles = []
    for url in news_processor.DAILY_BRIEF_URLS:
        # Fetch article details (simplified - in production would cache this)
        html_title, full_content, _ = news_processor.fetch_article_content(url)
        
        # Extract first paragraph as summary
        summary = full_content[:300] + "..." if len(full_content) > 300 else full_content
        
        brief_articles.append({
            'title': html_title,
            'url': url,
            'summary': summary,
            'source': 'Various Sources'
        })
    
    logging.info(f"Collected {len(brief_articles)} articles for brief")
    
    # Generate brief content
    today = datetime.now()
    md_content = daily_brief_generator.generate_daily_brief_markdown(brief_articles, today)
    
    # Convert to HTML
    html_content = daily_brief_generator.convert_markdown_to_html(md_content, today)
    
    # Generate metadata
    metadata = daily_brief_generator.generate_brief_metadata(md_content, today)
    
    # Publish to GitHub Pages
    github_manager.publish_brief_to_github_pages(REPO_NAME, html_content, today)
    
    # Update briefs index
    briefs_index = {
        'latest': metadata,
        'archive': [metadata]  # In production, would append to existing archive
    }
    github_manager.update_github_pages_json(REPO_NAME, [], briefs_index)
    
    # Clear daily brief URLs and save state
    news_processor.DAILY_BRIEF_URLS.clear()
    state['daily_brief_urls'] = []
    state['last_brief_date'] = today.isoformat()
    github_manager.save_bot_state(state)
    github_manager.push_state_to_github(REPO_NAME)
    
    logging.info("=== Daily brief published successfully ===")


if __name__ == "__main__":
    try:
        generate_and_publish_brief()
    except Exception as e:
        logging.error(f"Brief generation failed: {e}", exc_info=True)
        raise
