# twitter_publisher.py
import os
import tweepy
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class TwitterPublisher:
    """Handles publishing tweets to Twitter using Tweepy."""
    
    def __init__(self):
        """Initialize Twitter API client with authentication."""
        # Initialize with v2 client
        self.client = tweepy.Client(
            bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_API_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_SECRET")
        )
        
        # Initialize v1.1 API for media upload if needed
        auth = tweepy.OAuth1UserHandler(
            os.getenv("TWITTER_API_KEY"),
            os.getenv("TWITTER_API_SECRET"),
            os.getenv("TWITTER_ACCESS_TOKEN"),
            os.getenv("TWITTER_ACCESS_SECRET")
        )
        self.api_v1 = tweepy.API(auth)
    
    def publish_tweet(self, content: str, article_url: str, image_path: Optional[str] = None) -> bool:
        """
        Publish a tweet with the given content, URL, and optional image.
        
        Args:
            content: The tweet text (headline and summary)
            article_url: URL of the article to include
            image_path: Optional path to image file to attach
            
        Returns:
            True if tweet was published successfully, False otherwise
        """
        try:
            # Construct full tweet text
            tweet_text = f"{content}\n\n{article_url}"
            
            # Ensure tweet is within character limit (280 chars)
            if len(tweet_text) > 280:
                # Truncate content to fit
                available_chars = 280 - len(article_url) - 3  # 3 for "\n\n" and buffer
                content = content[:available_chars - 3] + "..."
                tweet_text = f"{content}\n\n{article_url}"
            
            # Upload media if image provided
            media_ids = []
            if image_path and os.path.exists(image_path):
                try:
                    media = self.api_v1.media_upload(filename=image_path)
                    media_ids.append(media.media_id)
                except Exception as e:
                    print(f"DEBUG: Error uploading media: {e}")
            
            # Publish tweet
            if media_ids:
                response = self.client.create_tweet(text=tweet_text, media_ids=media_ids)
            else:
                response = self.client.create_tweet(text=tweet_text)
            
            print(f"DEBUG: Tweet published successfully: {response.data}")
            return True
            
        except Exception as e:
            print(f"DEBUG: Error publishing tweet: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Test Twitter API connection."""
        try:
            # Try to get authenticated user info
            me = self.client.get_me()
            print(f"DEBUG: Twitter connection successful. Authenticated as: {me.data}")
            return True
        except Exception as e:
            print(f"DEBUG: Twitter connection failed: {e}")
            return False
