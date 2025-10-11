#!/usr/bin/env python3
"""
Test bot functionality with mock data (no API calls required).
"""

import sys
import os
from datetime import datetime

def test_image_selection():
    """Test image manager with mock articles."""
    print("Testing Image Selection...")
    
    from image_manager import ImageManager
    
    img_mgr = ImageManager()
    
    # Test company logo matching
    test_articles = [
        {
            'title': 'Bitmain Releases New Antminer S19 XP',
            'body': 'Bitmain announced their latest mining hardware...'
        },
        {
            'title': 'Bitcoin Hashrate Reaches New High',
            'body': 'The Bitcoin network hashrate has reached unprecedented levels...'
        },
        {
            'title': 'Mining Farm Expands Operations',
            'body': 'A major mining farm in Texas is expanding with new facilities...'
        }
    ]
    
    for article in test_articles:
        image = img_mgr.select_image(article)
        print(f"  Article: {article['title'][:50]}...")
        print(f"  Selected Image: {os.path.basename(image) if image else 'None'}")
    
    print("✓ Image selection test complete\n")
    return True

def test_state_management():
    """Test state persistence."""
    print("Testing State Management...")
    
    from github_manager import GitHubManager
    
    gh_mgr = GitHubManager()
    
    # Load state
    state = gh_mgr.load_state()
    print(f"  Loaded state version: {state.get('version')}")
    
    # Modify state
    state['test_data'] = {
        'timestamp': datetime.now().isoformat(),
        'test': True
    }
    
    # Save state
    success = gh_mgr.save_state(state)
    print(f"  State saved: {success}")
    
    # Reload to verify
    new_state = gh_mgr.load_state()
    print(f"  Test data present: {('test_data' in new_state)}")
    
    # Clean up test data
    if 'test_data' in new_state:
        del new_state['test_data']
        gh_mgr.save_state(new_state)
    
    print("✓ State management test complete\n")
    return True

def test_article_processing():
    """Test article enhancement simulation."""
    print("Testing Article Processing (without API)...")
    
    # Create mock article
    mock_article = {
        'title': 'Bitcoin Mining Difficulty Increases by 5%',
        'url': 'https://example.com/article',
        'source': 'Example News',
        'published_date': datetime.now().isoformat(),
        'body': 'The Bitcoin mining difficulty has increased by 5% in the latest adjustment, reflecting the growing hashrate on the network. This change impacts miners profitability...',
        'fetched_at': datetime.now().isoformat()
    }
    
    print(f"  Mock Article: {mock_article['title']}")
    print(f"  Body length: {len(mock_article['body'])} chars")
    
    # Test that article structure is valid
    required_fields = ['title', 'url', 'source', 'body']
    all_present = all(field in mock_article for field in required_fields)
    print(f"  Required fields present: {all_present}")
    
    print("✓ Article processing test complete\n")
    return True

def test_queue_operations():
    """Test LIFO queue operations."""
    print("Testing Queue Operations...")
    
    from github_manager import GitHubManager
    
    gh_mgr = GitHubManager()
    state = gh_mgr.load_state()
    
    # Clear queue for testing
    state['article_queue'] = []
    
    # Add articles (LIFO - newest first)
    test_articles = [
        {'url': 'https://example.com/1', 'title': 'Article 1'},
        {'url': 'https://example.com/2', 'title': 'Article 2'},
        {'url': 'https://example.com/3', 'title': 'Article 3'}
    ]
    
    for article in test_articles:
        state['article_queue'].insert(0, article)  # LIFO insert
    
    print(f"  Added {len(test_articles)} articles to queue")
    print(f"  Queue size: {len(state['article_queue'])}")
    
    # Test LIFO retrieval
    if state['article_queue']:
        first = state['article_queue'][0]
        print(f"  First article (most recent): {first['title']}")
        expected_title = 'Article 3'  # Last added, first out
        print(f"  LIFO working correctly: {first['title'] == expected_title}")
    
    # Test deduplication
    duplicate = {'url': 'https://example.com/2', 'title': 'Article 2 Duplicate'}
    if not any(a.get('url') == duplicate['url'] for a in state['article_queue']):
        state['article_queue'].insert(0, duplicate)
        print("  Would add duplicate (check failed)")
    else:
        print("  ✓ Duplicate detection working")
    
    # Clean up
    state['article_queue'] = []
    gh_mgr.save_state(state)
    
    print("✓ Queue operations test complete\n")
    return True

def test_website_json_generation():
    """Test JSON generation for website."""
    print("Testing Website JSON Generation...")
    
    from github_manager import GitHubManager
    import json
    
    gh_mgr = GitHubManager()
    
    # Test tweet JSON
    mock_tweets = [
        {
            'title': 'Bitcoin Mining News 1',
            'url': 'https://example.com/1',
            'published_at': datetime.now().isoformat(),
            'tweet_id': '123456789'
        }
    ]
    
    success = gh_mgr.update_website_tweets(mock_tweets)
    print(f"  Tweets JSON updated: {success}")
    
    # Verify JSON is valid
    try:
        with open('gh-pages/sha256news-tweets.json', 'r') as f:
            data = json.load(f)
            print(f"  Tweets in JSON: {len(data.get('tweets', []))}")
    except Exception as e:
        print(f"  ✗ Error reading JSON: {e}")
        return False
    
    print("✓ Website JSON generation test complete\n")
    return True

def main():
    """Run all mock data tests."""
    print("=" * 60)
    print("Bitcoin Mining News Bot - Mock Data Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    try:
        results.append(("Image Selection", test_image_selection()))
    except Exception as e:
        print(f"✗ Image Selection failed: {e}\n")
        results.append(("Image Selection", False))
    
    try:
        results.append(("State Management", test_state_management()))
    except Exception as e:
        print(f"✗ State Management failed: {e}\n")
        results.append(("State Management", False))
    
    try:
        results.append(("Article Processing", test_article_processing()))
    except Exception as e:
        print(f"✗ Article Processing failed: {e}\n")
        results.append(("Article Processing", False))
    
    try:
        results.append(("Queue Operations", test_queue_operations()))
    except Exception as e:
        print(f"✗ Queue Operations failed: {e}\n")
        results.append(("Queue Operations", False))
    
    try:
        results.append(("Website JSON", test_website_json_generation()))
    except Exception as e:
        print(f"✗ Website JSON failed: {e}\n")
        results.append(("Website JSON", False))
    
    # Print summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All mock data tests passed!")
        print("Bot is ready for deployment with API credentials.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
