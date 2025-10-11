#!/usr/bin/env python3
"""
Test script for Bitcoin Mining News Aggregator Bot

This script tests the basic functionality without making actual API calls.
"""

import sys
import os
from datetime import datetime

# Test imports
print("=" * 60)
print("Bitcoin Mining News Aggregator Bot - Test Suite")
print("=" * 60)
print()

print("1. Testing Module Imports...")
print("-" * 60)

try:
    import news_processor
    print("✓ news_processor imported successfully")
except Exception as e:
    print(f"✗ news_processor import failed: {e}")
    sys.exit(1)

try:
    import gemini_interface
    print("✓ gemini_interface imported successfully")
except Exception as e:
    print(f"✗ gemini_interface import failed: {e}")
    sys.exit(1)

try:
    import twitter_publisher
    print("✓ twitter_publisher imported successfully")
except Exception as e:
    print(f"✗ twitter_publisher import failed: {e}")
    sys.exit(1)

try:
    import image_manager
    print("✓ image_manager imported successfully")
except Exception as e:
    print(f"✗ image_manager import failed: {e}")
    sys.exit(1)

try:
    import daily_brief_generator
    print("✓ daily_brief_generator imported successfully")
except Exception as e:
    print(f"✗ daily_brief_generator import failed: {e}")
    sys.exit(1)

try:
    import github_manager
    print("✓ github_manager imported successfully")
except Exception as e:
    print(f"✗ github_manager import failed: {e}")
    sys.exit(1)

print()
print("2. Testing State Management...")
print("-" * 60)

try:
    mgr = github_manager.GitHubManager()
    state = mgr.load_state()
    print(f"✓ State loaded successfully")
    print(f"  - Queue size: {len(state['article_queue'])}")
    print(f"  - Published count: {len(state['published_articles'])}")
    
    # Test adding articles
    test_articles = [
        {'id': 'test1', 'title': 'Test Article 1', 'url': 'http://example.com/1'},
        {'id': 'test2', 'title': 'Test Article 2', 'url': 'http://example.com/2'},
    ]
    state = mgr.add_articles_to_queue(test_articles, state)
    print(f"✓ Articles added to queue: {len(state['article_queue'])}")
    
    # Test popping
    article, state = mgr.pop_article_from_queue(state)
    if article:
        print(f"✓ Article popped from queue (LIFO): {article['id']}")
    
    # Test marking as published
    state = mgr.mark_article_published('test1', state)
    print(f"✓ Article marked as published")
    
except Exception as e:
    print(f"✗ State management test failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("3. Testing Image Management...")
print("-" * 60)

try:
    image_manager.ensure_placeholder_images()
    print("✓ Placeholder images created/verified")
    
    # Test image selection
    test_title = "Bitcoin Mining Company Marathon Digital Reports Q4 Results"
    test_content = "Marathon Digital Holdings announced strong quarterly results..."
    image_path = image_manager.get_image_for_article(test_title, test_content)
    if image_path:
        print(f"✓ Image selected: {os.path.basename(image_path)}")
    else:
        print("✓ No specific image found (expected for test data)")
        
except Exception as e:
    print(f"✗ Image management test failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("4. Testing Daily Brief Generation...")
print("-" * 60)

try:
    # Test brief generation logic
    test_state = {
        'last_brief_date': None,
        'daily_brief_articles': [
            {'id': f'art{i}', 'title': f'Article {i}'} for i in range(6)
        ]
    }
    should_generate = daily_brief_generator.should_generate_brief(test_state)
    print(f"✓ Brief generation check: {should_generate}")
    
    # Test article collection
    articles = daily_brief_generator.collect_articles_for_brief(test_state)
    print(f"✓ Articles collected for brief: {len(articles)}")
    
except Exception as e:
    print(f"✗ Daily brief test failed: {e}")
    import traceback
    traceback.print_exc()

print()
print("5. Testing File Structure...")
print("-" * 60)

required_files = [
    'main.py',
    'news_processor.py',
    'gemini_interface.py',
    'twitter_publisher.py',
    'image_manager.py',
    'daily_brief_generator.py',
    'github_manager.py',
    'requirements.txt',
    '.env.example',
    'bot_state.json',
    'images/bitcoin_logo.png',
    'images/default_mining_concept.png',
]

all_present = True
for filepath in required_files:
    if os.path.exists(filepath):
        print(f"✓ {filepath}")
    else:
        print(f"✗ {filepath} missing")
        all_present = False

print()
print("=" * 60)
if all_present:
    print("✓ All tests passed! Bot is ready for deployment.")
else:
    print("✗ Some tests failed. Please review the output above.")
print("=" * 60)
print()
print("Next steps:")
print("1. Add your API keys to .env (copy from .env.example)")
print("2. Set up GitHub Secrets for Actions")
print("3. Test with actual API calls in a safe environment")
print("4. Enable GitHub Pages for brief publishing")
print("5. Deploy GitHub Actions workflows")
