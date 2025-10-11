"""
Twitter Publisher Module

Handles publishing content to Twitter/X:
- Tweet composition with text and images
- Media upload
- Rate limiting and error handling
- Tweet threading support
"""

import os
import logging
import tweepy
from datetime import datetime

logger = logging.getLogger(__name__)


class TwitterPublisher:
    """Publish content to Twitter."""
    
    def __init__(self):
        """Initialize Twitter API client."""
        try:
            # Twitter API v2 with OAuth 1.0a
            api_key = os.getenv('TWITTER_API_KEY')
            api_secret = os.getenv('TWITTER_API_SECRET')
            access_token = os.getenv('TWITTER_ACCESS_TOKEN')
            access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            
            if not all([api_key, api_secret, access_token, access_token_secret]):
                logger.warning("Twitter credentials not fully configured")
                self.client = None
                self.api = None
                return
            
            # Initialize v2 client
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret
            )
            
            # Initialize v1.1 API for media upload
            auth = tweepy.OAuth1UserHandler(
                api_key, api_secret,
                access_token, access_token_secret
            )
            self.api = tweepy.API(auth)
            
            logger.info("Twitter client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Twitter client: {e}", exc_info=True)
            self.client = None
            self.api = None
    
    def publish_tweet(self, content, image_path=None, article_url=None):
        """
        Publish a tweet with optional image.
        
        Args:
            content: Tweet text content
            image_path: Optional path to image file
            article_url: Optional URL to append
            
        Returns:
            Dictionary with tweet result or None on failure
        """
        if not self.client:
            logger.warning("Twitter client not configured, skipping tweet")
            return None
        
        try:
            # Prepare tweet text
            tweet_text = content
            
            # Add URL if provided and space allows
            if article_url:
                # Twitter auto-shortens URLs to ~23 chars
                if len(tweet_text) + 24 <= 280:  # Leave space for URL
                    tweet_text += f"\n\n{article_url}"
                elif len(tweet_text) > 256:
                    # Truncate content to make room for URL
                    tweet_text = tweet_text[:253] + f"...\n\n{article_url}"
            
            # Upload media if provided
            media_ids = []
            if image_path and os.path.exists(image_path):
                try:
                    media = self.api.media_upload(filename=image_path)
                    media_ids.append(media.media_id)
                    logger.info(f"Uploaded media: {image_path}")
                except Exception as e:
                    logger.warning(f"Could not upload media: {e}")
            
            # Create tweet
            response = self.client.create_tweet(
                text=tweet_text,
                media_ids=media_ids if media_ids else None
            )
            
            tweet_id = response.data['id']
            logger.info(f"Tweet published successfully: {tweet_id}")
            
            return {
                'id': tweet_id,
                'text': tweet_text,
                'published_at': datetime.now().isoformat()
            }
            
        except tweepy.errors.TweepyException as e:
            logger.error(f"Twitter API error: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error publishing tweet: {e}", exc_info=True)
            return None
    
    def publish_thread(self, tweets_content, image_paths=None):
        """
        Publish a thread of tweets.
        
        Args:
            tweets_content: List of tweet text strings
            image_paths: Optional list of image paths (aligned with tweets)
            
        Returns:
            List of tweet result dictionaries
        """
        if not self.client:
            logger.warning("Twitter client not configured, skipping thread")
            return []
        
        results = []
        previous_tweet_id = None
        
        for i, content in enumerate(tweets_content):
            try:
                # Get corresponding image if available
                image_path = None
                if image_paths and i < len(image_paths):
                    image_path = image_paths[i]
                
                # Upload media if provided
                media_ids = []
                if image_path and os.path.exists(image_path):
                    try:
                        media = self.api.media_upload(filename=image_path)
                        media_ids.append(media.media_id)
                    except Exception as e:
                        logger.warning(f"Could not upload media for thread: {e}")
                
                # Create tweet in thread
                response = self.client.create_tweet(
                    text=content,
                    media_ids=media_ids if media_ids else None,
                    in_reply_to_tweet_id=previous_tweet_id
                )
                
                tweet_id = response.data['id']
                previous_tweet_id = tweet_id
                
                results.append({
                    'id': tweet_id,
                    'text': content,
                    'position': i + 1,
                    'published_at': datetime.now().isoformat()
                })
                
                logger.info(f"Thread tweet {i + 1}/{len(tweets_content)} published: {tweet_id}")
                
            except Exception as e:
                logger.error(f"Error publishing thread tweet {i + 1}: {e}", exc_info=True)
                break  # Stop thread on error
        
        logger.info(f"Thread published: {len(results)}/{len(tweets_content)} tweets")
        return results
    
    def delete_tweet(self, tweet_id):
        """
        Delete a tweet by ID.
        
        Args:
            tweet_id: Twitter tweet ID
            
        Returns:
            Boolean success status
        """
        if not self.client:
            logger.warning("Twitter client not configured")
            return False
        
        try:
            self.client.delete_tweet(tweet_id)
            logger.info(f"Deleted tweet: {tweet_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting tweet {tweet_id}: {e}", exc_info=True)
            return False
