#!/usr/bin/env python3
"""
Test script to verify bot structure without requiring API keys.
Tests basic functionality and structure of all modules.
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        import main
        print("✓ main.py imported")
    except Exception as e:
        print(f"✗ main.py import failed: {e}")
        return False
    
    try:
        from news_processor import NewsProcessor
        print("✓ news_processor.py imported")
    except Exception as e:
        print(f"✗ news_processor.py import failed: {e}")
        return False
    
    try:
        from gemini_interface import GeminiInterface
        print("✓ gemini_interface.py imported")
    except Exception as e:
        print(f"✗ gemini_interface.py import failed: {e}")
        return False
    
    try:
        from twitter_publisher import TwitterPublisher
        print("✓ twitter_publisher.py imported")
    except Exception as e:
        print(f"✗ twitter_publisher.py import failed: {e}")
        return False
    
    try:
        from image_manager import ImageManager
        print("✓ image_manager.py imported")
    except Exception as e:
        print(f"✗ image_manager.py import failed: {e}")
        return False
    
    try:
        from daily_brief_generator import DailyBriefGenerator
        print("✓ daily_brief_generator.py imported")
    except Exception as e:
        print(f"✗ daily_brief_generator.py import failed: {e}")
        return False
    
    try:
        from github_manager import GitHubManager
        print("✓ github_manager.py imported")
    except Exception as e:
        print(f"✗ github_manager.py import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without API calls."""
    print("\nTesting basic functionality...")
    
    try:
        from image_manager import ImageManager
        img_mgr = ImageManager()
        available = img_mgr.list_available_images()
        print(f"✓ ImageManager initialized, found {len(available['conceptual'])} conceptual images")
    except Exception as e:
        print(f"✗ ImageManager test failed: {e}")
        return False
    
    try:
        from github_manager import GitHubManager
        gh_mgr = GitHubManager()
        state = gh_mgr.load_state()
        print(f"✓ GitHubManager initialized, state version: {state.get('version', 'unknown')}")
    except Exception as e:
        print(f"✗ GitHubManager test failed: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    
    required_dirs = [
        'images/conceptual',
        'images/company_logos',
        'gh-pages',
        'gh-pages/briefs',
        '.github/workflows'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        if os.path.exists(full_path):
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} missing")
            all_exist = False
    
    return all_exist

def test_required_files():
    """Test that required files exist."""
    print("\nTesting required files...")
    
    required_files = [
        'requirements.txt',
        '.env.example',
        'README.md',
        'MODEL_CONTEXT_PROTOCOL.md',
        'copilot_instructions.md',
        'gh-pages/index.html',
        'gh-pages/brief_template.html',
        'gh-pages/sha256news-tweets.json',
        'gh-pages/briefs_index.json',
        '.github/workflows/main.yml',
        '.github/workflows/publish_brief.yml'
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests."""
    print("=" * 60)
    print("Bitcoin Mining News Bot - Structure Test")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Directory Structure", test_directory_structure()))
    results.append(("Required Files", test_required_files()))
    
    # Print summary
    print("\n" + "=" * 60)
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
        print("\n✓ All tests passed! Bot structure is ready.")
        return 0
    else:
        print("\n✗ Some tests failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
