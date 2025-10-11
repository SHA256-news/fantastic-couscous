#!/usr/bin/env python3
# main.py
"""
Bitcoin-Only Mining News Aggregator Bot

This bot automatically:
1. Fetches Bitcoin mining news from EventRegistry
2. Filters articles using AI (Gemini) for relevance
3. Generates tweet content using AI
4. Publishes tweets every 90 minutes using LIFO queue
5. Generates daily briefs and creates GitHub issues for review
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from news_processor import fetch_articles_from_eventregistry, process_articles
from gemini_interface import semantically_filter_article, generate_tweet_content
from twitter_publisher import TwitterPublisher
from image_manager import get_image_for_article, ensure_placeholder_images
from daily_brief_generator import generate_daily_brief, should_generate_brief, collect_articles_for_brief
from github_manager import GitHubManager

load_dotenv()


def main():
    """Main bot execution function."""
    print(f"=== Bitcoin Mining News Aggregator Bot ===")
    print(f"Execution time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize managers
    github_mgr = GitHubManager()
    twitter_pub = TwitterPublisher()
    
    # Ensure placeholder images exist
    ensure_placeholder_images()
    
    # Load bot state
    state = github_mgr.load_state()
    print(f"DEBUG: Current queue size: {len(state['article_queue'])}")
    print(f"DEBUG: Published articles count: {len(state['published_articles'])}")
    
    # Step 1: Fetch new articles (every run)
    print("\n--- Fetching new articles ---")
    raw_articles = fetch_articles_from_eventregistry(hours_back=2)
    print(f"DEBUG: Fetched {len(raw_articles)} raw articles from EventRegistry")
    
    # Step 2: Process and filter articles
    if raw_articles:
        print("\n--- Processing and filtering articles ---")
        relevant_articles = process_articles(raw_articles, semantically_filter_article)
        print(f"DEBUG: {len(relevant_articles)} articles marked as relevant")
        
        # Add to queue and daily brief collection
        if relevant_articles:
            state = github_mgr.add_articles_to_queue(relevant_articles, state)
            
            # Also add to daily brief collection
            if 'daily_brief_articles' not in state:
                state['daily_brief_articles'] = []
            
            for article in relevant_articles:
                # Avoid duplicates in daily brief collection
                article_ids = {a.get('id') for a in state['daily_brief_articles']}
                if article.get('id') not in article_ids:
                    state['daily_brief_articles'].append(article)
            
            state['last_fetch_time'] = datetime.now().isoformat()
            github_mgr.save_state(state)
    
    # Step 3: Check if we should generate daily brief
    if should_generate_brief(state):
        print("\n--- Generating daily brief ---")
        today = datetime.now().strftime('%Y-%m-%d')
        brief_articles = collect_articles_for_brief(state)
        
        brief_content = generate_daily_brief(brief_articles, today)
        print(f"DEBUG: Generated brief with {len(brief_articles)} articles")
        
        # Create GitHub issue for review
        repo_name = github_mgr.get_repo_name_from_context()
        success = github_mgr.create_daily_brief_issue(brief_content, today, repo_name)
        
        if success:
            # Mark brief as generated for today
            state['last_brief_date'] = today
            # Clear the daily brief articles collection
            state['daily_brief_articles'] = []
            github_mgr.save_state(state)
            print("DEBUG: Daily brief issue created successfully")
        else:
            print("DEBUG: Failed to create daily brief issue")
    
    # Step 4: Publish a tweet if queue has articles
    if state['article_queue']:
        print("\n--- Publishing tweet ---")
        
        # Pop article from LIFO queue
        article, state = github_mgr.pop_article_from_queue(state)
        
        if article:
            print(f"DEBUG: Processing article: {article.get('title', 'N/A')}")
            
            # Generate tweet content
            tweet_content = generate_tweet_content(
                article.get('title', ''),
                article.get('full_text', article.get('body', '')),
                article.get('title', '')
            )
            
            # Get appropriate image
            image_path = get_image_for_article(
                article.get('title', ''),
                article.get('full_text', article.get('body', ''))
            )
            
            # Publish tweet
            success = twitter_pub.publish_tweet(
                tweet_content,
                article.get('url', ''),
                image_path
            )
            
            if success:
                # Mark as published
                state = github_mgr.mark_article_published(article.get('id', ''), state)
                print("DEBUG: Tweet published successfully")
            else:
                # If failed, put article back in queue
                state['article_queue'].append(article)
                print("DEBUG: Tweet publishing failed, article returned to queue")
            
            github_mgr.save_state(state)
    else:
        print("\n--- No articles in queue to tweet ---")
    
    print("\n=== Bot execution completed ===")
    print(f"Final queue size: {len(state['article_queue'])}")


if __name__ == "__main__":
    main()
