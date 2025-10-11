# github_manager.py
import os
import json
import logging
from datetime import datetime
from typing import Dict, List
from github import Github, GithubException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GH_PAT = os.getenv("GH_PAT")
BOT_STATE_FILE = "bot_state.json"


def load_bot_state() -> Dict:
    """
    Loads bot state from bot_state.json file.
    Returns default state if file doesn't exist or is invalid.
    """
    default_state = {
        'processed_urls': [],
        'processed_event_uris': [],
        'daily_brief_urls': [],
        'lifo_queue': [],
        'last_run': None,
        'last_brief_date': None
    }
    
    if not os.path.exists(BOT_STATE_FILE):
        logging.info("bot_state.json not found, starting with fresh state.")
        return default_state
    
    try:
        with open(BOT_STATE_FILE, 'r') as f:
            state = json.load(f)
        logging.info("Loaded bot state from bot_state.json")
        return state
    except Exception as e:
        logging.error(f"Error loading bot_state.json: {e}. Using default state.")
        return default_state


def save_bot_state(state: Dict):
    """
    Saves bot state to bot_state.json file.
    """
    try:
        with open(BOT_STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        logging.info("Saved bot state to bot_state.json")
    except Exception as e:
        logging.error(f"Error saving bot_state.json: {e}")


def push_state_to_github(repo_name: str, commit_message: str = "Update bot state"):
    """
    Pushes bot_state.json to GitHub repository.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        commit_message: Commit message for the update
    """
    if not GH_PAT:
        logging.warning("GH_PAT not configured. Cannot push state to GitHub.")
        return
    
    try:
        g = Github(GH_PAT)
        repo = g.get_repo(repo_name)
        
        # Read current state file
        with open(BOT_STATE_FILE, 'r') as f:
            content = f.read()
        
        # Try to get existing file
        try:
            file = repo.get_contents(BOT_STATE_FILE)
            repo.update_file(
                BOT_STATE_FILE,
                commit_message,
                content,
                file.sha
            )
            logging.info(f"Updated {BOT_STATE_FILE} in GitHub")
        except GithubException:
            # File doesn't exist, create it
            repo.create_file(
                BOT_STATE_FILE,
                commit_message,
                content
            )
            logging.info(f"Created {BOT_STATE_FILE} in GitHub")
    
    except Exception as e:
        logging.error(f"Error pushing state to GitHub: {e}")


def update_github_pages_json(repo_name: str, tweets_data: List[Dict], briefs_index: Dict = None):
    """
    Updates JSON files in gh-pages branch for website widgets.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        tweets_data: List of recent tweet data dicts
        briefs_index: Optional dict with briefs index data
    """
    if not GH_PAT:
        logging.warning("GH_PAT not configured. Cannot update GitHub Pages.")
        return
    
    try:
        g = Github(GH_PAT)
        repo = g.get_repo(repo_name)
        
        # Update sha256news-tweets.json
        tweets_json = json.dumps(tweets_data, indent=2)
        tweets_file_path = "gh-pages/sha256news-tweets.json"
        
        try:
            file = repo.get_contents(tweets_file_path)
            repo.update_file(
                tweets_file_path,
                "Update latest tweets",
                tweets_json,
                file.sha
            )
            logging.info(f"Updated {tweets_file_path} in GitHub")
        except GithubException:
            repo.create_file(
                tweets_file_path,
                "Create tweets JSON",
                tweets_json
            )
            logging.info(f"Created {tweets_file_path} in GitHub")
        
        # Update briefs_index.json if provided
        if briefs_index:
            briefs_json = json.dumps(briefs_index, indent=2)
            briefs_file_path = "gh-pages/briefs_index.json"
            
            try:
                file = repo.get_contents(briefs_file_path)
                repo.update_file(
                    briefs_file_path,
                    "Update briefs index",
                    briefs_json,
                    file.sha
                )
                logging.info(f"Updated {briefs_file_path} in GitHub")
            except GithubException:
                repo.create_file(
                    briefs_file_path,
                    "Create briefs index JSON",
                    briefs_json
                )
                logging.info(f"Created {briefs_file_path} in GitHub")
    
    except Exception as e:
        logging.error(f"Error updating GitHub Pages JSON: {e}")


def publish_brief_to_github_pages(repo_name: str, brief_html: str, brief_date: datetime):
    """
    Publishes a daily brief HTML file to gh-pages branch.
    
    Args:
        repo_name: Full repository name (e.g., "owner/repo")
        brief_html: HTML content of the brief
        brief_date: Date of the brief
    """
    if not GH_PAT:
        logging.warning("GH_PAT not configured. Cannot publish brief to GitHub Pages.")
        return
    
    try:
        g = Github(GH_PAT)
        repo = g.get_repo(repo_name)
        
        date_str = brief_date.strftime("%Y-%m-%d")
        file_path = f"gh-pages/briefs/brief-{date_str}.html"
        
        try:
            file = repo.get_contents(file_path)
            repo.update_file(
                file_path,
                f"Update daily brief for {date_str}",
                brief_html,
                file.sha
            )
            logging.info(f"Updated brief {file_path} in GitHub Pages")
        except GithubException:
            repo.create_file(
                file_path,
                f"Publish daily brief for {date_str}",
                brief_html
            )
            logging.info(f"Published brief {file_path} to GitHub Pages")
    
    except Exception as e:
        logging.error(f"Error publishing brief to GitHub Pages: {e}")
