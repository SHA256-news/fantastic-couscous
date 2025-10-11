"""
GitHub Manager Module

Handles GitHub integration:
- Bot state persistence (bot_state.json)
- GitHub Pages updates
- JSON file generation for website widgets
- Repository management
"""

import os
import logging
import json
from datetime import datetime
from github import Github, GithubException

logger = logging.getLogger(__name__)


class GitHubManager:
    """Manage GitHub integration and state persistence."""
    
    def __init__(self):
        """Initialize GitHub manager."""
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('GITHUB_REPO')
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.state_file = os.path.join(self.base_dir, 'bot_state.json')
        self.gh_pages_dir = os.path.join(self.base_dir, 'gh-pages')
        
        # GitHub API client
        self.github = None
        self.repo = None
        
        if self.github_token and self.repo_name:
            try:
                self.github = Github(self.github_token)
                self.repo = self.github.get_repo(self.repo_name)
                logger.info(f"GitHub integration enabled for {self.repo_name}")
            except Exception as e:
                logger.warning(f"Could not initialize GitHub API: {e}")
        else:
            logger.warning("GitHub credentials not configured, using local state only")
        
        # Ensure directories exist
        os.makedirs(self.gh_pages_dir, exist_ok=True)
        
        logger.info("GitHubManager initialized")
    
    def load_state(self):
        """
        Load bot state from file.
        
        Returns:
            State dictionary
        """
        default_state = {
            'version': '1.0',
            'initialized_at': datetime.now().isoformat(),
            'last_run': None,
            'article_queue': [],
            'published_articles': [],
            'daily_briefs': []
        }
        
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    logger.info("Loaded bot state from file")
                    return state
            else:
                logger.info("No existing state file, using default state")
                return default_state
                
        except Exception as e:
            logger.error(f"Error loading state: {e}", exc_info=True)
            return default_state
    
    def save_state(self, state):
        """
        Save bot state to file.
        
        Args:
            state: State dictionary to save
            
        Returns:
            Boolean success status
        """
        try:
            # Update timestamp
            state['last_updated'] = datetime.now().isoformat()
            
            # Save to local file
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            logger.info("Saved bot state to file")
            
            # Optionally sync to GitHub
            if self.repo:
                try:
                    self._sync_state_to_github(state)
                except Exception as e:
                    logger.warning(f"Could not sync state to GitHub: {e}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving state: {e}", exc_info=True)
            return False
    
    def _sync_state_to_github(self, state):
        """
        Sync state to GitHub repository.
        
        Args:
            state: State dictionary
        """
        try:
            file_path = 'bitcoin_miner_bot/bot_state.json'
            content = json.dumps(state, indent=2, ensure_ascii=False)
            
            # Check if file exists
            try:
                file = self.repo.get_contents(file_path)
                # Update existing file
                self.repo.update_file(
                    file_path,
                    f"Update bot state - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    content,
                    file.sha
                )
                logger.info("Updated bot state on GitHub")
            except GithubException:
                # Create new file
                self.repo.create_file(
                    file_path,
                    f"Create bot state - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                    content
                )
                logger.info("Created bot state on GitHub")
                
        except Exception as e:
            logger.error(f"Error syncing state to GitHub: {e}", exc_info=True)
    
    def update_website_tweets(self, tweets):
        """
        Update website tweets JSON file.
        
        Args:
            tweets: List of tweet dictionaries
            
        Returns:
            Boolean success status
        """
        try:
            tweets_json_path = os.path.join(self.gh_pages_dir, 'sha256news-tweets.json')
            
            # Format tweets for website
            formatted_tweets = []
            for tweet in tweets:
                formatted_tweets.append({
                    'title': tweet.get('title', ''),
                    'url': tweet.get('url', ''),
                    'published_at': tweet.get('published_at', ''),
                    'tweet_id': tweet.get('tweet_id', '')
                })
            
            # Save to file
            with open(tweets_json_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'tweets': formatted_tweets,
                    'updated_at': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated website tweets JSON: {len(formatted_tweets)} tweets")
            return True
            
        except Exception as e:
            logger.error(f"Error updating website tweets: {e}", exc_info=True)
            return False
    
    def update_briefs_index(self, briefs):
        """
        Update briefs index JSON file.
        
        Args:
            briefs: List of brief metadata dictionaries
            
        Returns:
            Boolean success status
        """
        try:
            briefs_index_path = os.path.join(self.gh_pages_dir, 'briefs_index.json')
            
            # Prepare index data
            index_data = {
                'lead_article': briefs[0] if briefs else None,
                'archive': briefs[1:] if len(briefs) > 1 else [],
                'updated_at': datetime.now().isoformat()
            }
            
            # Save to file
            with open(briefs_index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Updated briefs index JSON: {len(briefs)} briefs")
            return True
            
        except Exception as e:
            logger.error(f"Error updating briefs index: {e}", exc_info=True)
            return False
    
    def commit_and_push_changes(self, message="Update bot data"):
        """
        Commit and push local changes to GitHub.
        
        Args:
            message: Commit message
            
        Returns:
            Boolean success status
        """
        if not self.repo:
            logger.warning("GitHub not configured, cannot push changes")
            return False
        
        try:
            # This is a simplified approach
            # In practice, you'd use git commands or PyGithub's more advanced features
            logger.info(f"Would commit and push with message: {message}")
            
            # For a real implementation, use subprocess to run git commands
            # or use PyGithub's tree/blob API
            
            return True
            
        except Exception as e:
            logger.error(f"Error committing changes: {e}", exc_info=True)
            return False
    
    def get_file_content(self, file_path):
        """
        Get content of a file from GitHub.
        
        Args:
            file_path: Path to file in repository
            
        Returns:
            File content string or None
        """
        if not self.repo:
            return None
        
        try:
            file = self.repo.get_contents(file_path)
            content = file.decoded_content.decode('utf-8')
            logger.info(f"Retrieved file from GitHub: {file_path}")
            return content
            
        except Exception as e:
            logger.warning(f"Could not get file from GitHub: {e}")
            return None
    
    def update_file(self, file_path, content, message):
        """
        Update a file on GitHub.
        
        Args:
            file_path: Path to file in repository
            content: New file content
            message: Commit message
            
        Returns:
            Boolean success status
        """
        if not self.repo:
            logger.warning("GitHub not configured")
            return False
        
        try:
            # Check if file exists
            try:
                file = self.repo.get_contents(file_path)
                # Update existing file
                self.repo.update_file(file_path, message, content, file.sha)
                logger.info(f"Updated file on GitHub: {file_path}")
            except GithubException:
                # Create new file
                self.repo.create_file(file_path, message, content)
                logger.info(f"Created file on GitHub: {file_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating file on GitHub: {e}", exc_info=True)
            return False
