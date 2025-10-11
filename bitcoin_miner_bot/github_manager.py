# github_manager.py
import os
import json
from typing import Dict, List, Any
from github import Github, GithubException
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# State file path
STATE_FILE = os.path.join(os.path.dirname(__file__), 'bot_state.json')


class GitHubManager:
    """Manages GitHub interactions for state persistence and issue creation."""
    
    def __init__(self):
        """Initialize GitHub API client."""
        self.github_token = os.getenv("GH_PAT")
        if self.github_token:
            self.github = Github(self.github_token)
        else:
            self.github = None
            print("DEBUG: No GitHub token provided, some features will be disabled")
    
    def load_state(self) -> Dict[str, Any]:
        """
        Load bot state from JSON file.
        
        Returns:
            Dictionary containing bot state
        """
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                print(f"DEBUG: State loaded from {STATE_FILE}")
                return state
            except Exception as e:
                print(f"DEBUG: Error loading state: {e}")
        
        # Return default state if file doesn't exist or error occurred
        return {
            'article_queue': [],  # LIFO queue for articles
            'published_articles': [],  # History of published article IDs
            'last_fetch_time': None,
            'last_brief_date': None,
            'daily_brief_articles': []
        }
    
    def save_state(self, state: Dict[str, Any]) -> bool:
        """
        Save bot state to JSON file.
        
        Args:
            state: Dictionary containing bot state
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f, indent=2)
            print(f"DEBUG: State saved to {STATE_FILE}")
            return True
        except Exception as e:
            print(f"DEBUG: Error saving state: {e}")
            return False
    
    def add_articles_to_queue(self, articles: List[Dict], state: Dict) -> Dict:
        """
        Add new articles to the LIFO queue, avoiding duplicates.
        
        Args:
            articles: List of article dictionaries
            state: Current bot state
            
        Returns:
            Updated state
        """
        existing_ids = {art.get('id') for art in state['article_queue']}
        existing_published = set(state['published_articles'])
        
        new_articles = []
        for article in articles:
            article_id = article.get('id')
            # Skip if already in queue or already published
            if article_id not in existing_ids and article_id not in existing_published:
                new_articles.append(article)
        
        # Add to the end (LIFO: we'll pop from the end)
        state['article_queue'].extend(new_articles)
        
        print(f"DEBUG: Added {len(new_articles)} new articles to queue. Total queue size: {len(state['article_queue'])}")
        return state
    
    def pop_article_from_queue(self, state: Dict) -> tuple:
        """
        Pop an article from the LIFO queue (Last In, First Out).
        
        Args:
            state: Current bot state
            
        Returns:
            Tuple of (article_dict, updated_state)
        """
        if state['article_queue']:
            # Pop from the end (LIFO)
            article = state['article_queue'].pop()
            return article, state
        return None, state
    
    def mark_article_published(self, article_id: str, state: Dict) -> Dict:
        """
        Mark an article as published by adding its ID to the published list.
        
        Args:
            article_id: Article ID
            state: Current bot state
            
        Returns:
            Updated state
        """
        if article_id not in state['published_articles']:
            state['published_articles'].append(article_id)
            # Keep only last 1000 published IDs to prevent unbounded growth
            if len(state['published_articles']) > 1000:
                state['published_articles'] = state['published_articles'][-1000:]
        return state
    
    def create_daily_brief_issue(self, brief_content: str, date: str, repo_name: str) -> bool:
        """
        Create a GitHub issue with the daily brief for review.
        
        Args:
            brief_content: The daily brief content (Markdown)
            date: Date string for the brief
            repo_name: Repository name (e.g., 'owner/repo')
            
        Returns:
            True if issue created successfully, False otherwise
        """
        if not self.github:
            print("DEBUG: GitHub not initialized, cannot create issue")
            return False
        
        try:
            repo = self.github.get_repo(repo_name)
            
            title = f"Daily Bitcoin Mining Brief - {date}"
            body = f"## Daily Brief for {date}\n\n{brief_content}\n\n---\n\n**Instructions:** Review the brief above. If approved, close this issue to trigger automatic publication to GitHub Pages."
            
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=['daily-brief', 'review-needed']
            )
            
            print(f"DEBUG: Created issue #{issue.number}: {title}")
            return True
            
        except GithubException as e:
            print(f"DEBUG: Error creating GitHub issue: {e}")
            return False
    
    def get_repo_name_from_context(self) -> str:
        """
        Get repository name from environment variables or GitHub Actions context.
        
        Returns:
            Repository name in format 'owner/repo'
        """
        # Try GitHub Actions environment variables
        github_repo = os.getenv('GITHUB_REPOSITORY')
        if github_repo:
            return github_repo
        
        # Fallback to manual configuration
        return os.getenv('GITHUB_REPO_NAME', 'owner/repo')
