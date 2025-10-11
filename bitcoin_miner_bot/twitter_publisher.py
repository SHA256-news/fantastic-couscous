# twitter_publisher.py
import tweepy
import os
import logging
from dotenv import load_dotenv
from datetime import datetime  # For tweet timestamp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# Twitter API credentials
CONSUMER_KEY = os.getenv("TWITTER_API_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")  # For tweepy.Client
TWITTER_USERNAME_CONFIG = os.getenv("TWITTER_USERNAME", "SHA256News")  # Bot's handle from config

# Cache for the bot's own username (fetched once)
_cached_username = None


def get_twitter_client_v2():
    """Returns a tweepy.Client (v2 API) instance."""
    if not BEARER_TOKEN:
        logging.warning("BEARER_TOKEN not found. V2 client might not work for all operations.")
    return tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )


def get_twitter_api_v1_1():
    """Returns a tweepy.API (v1.1 API) instance for media uploads."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


def get_bot_username() -> str:
    """Fetches and caches the bot's Twitter username."""
    global _cached_username
    if _cached_username:
        return _cached_username
    try:
        client = get_twitter_client_v2()
        me = client.get_me()
        if me.data:
            _cached_username = me.data['username']
            logging.info(f"Fetched bot username: {_cached_username}")
            return _cached_username
    except Exception as e:
        logging.error(f"Could not fetch bot username via API: {e}. Using configured default.")
    return TWITTER_USERNAME_CONFIG  # Fallback to config


def upload_and_attach_images(api_v1_1, image_paths: list[str]) -> tuple[list[str], list[str]]:
    """
    Uploads images to Twitter and returns a list of media_ids and a list of relative image URLs
    suitable for GitHub Pages.
    """
    media_ids = []
    # Store GitHub Pages relative URLs for the images
    # e.g., 'images/conceptual/bitcoin_logo.png' -> '/images/conceptual/bitcoin_logo.png' (from gh-pages root)
    uploaded_image_relative_paths = []

    for path in image_paths:
        if not os.path.exists(path):
            logging.warning(f"Image file not found: {path}")
            continue
        try:
            media = api_v1_1.media_upload(filename=path)
            media_ids.append(media.media_id_string)
            
            # Construct relative URL for GitHub Pages. Assumes 'images/' is at repo root
            # and that gh-pages is the root of the website.
            relative_url_for_ghpages = f"/{path}"  # Prepends '/' for absolute path from website root
            uploaded_image_relative_paths.append(relative_url_for_ghpages)
            logging.debug(f"Uploaded {path}, media_id: {media.media_id_string}")
        except Exception as e:
            logging.error(f"Error uploading image {path}: {e}")
    return media_ids, uploaded_image_relative_paths


def publish_tweet(tweet_text: str, article_url: str, image_paths: list[str] = None) -> tuple[bool, dict | None]:
    """
    Publishes a tweet with generated content and attaches images.
    The source URL is included in a reply tweet to keep the main tweet within character limits.
    Returns (True, tweet_data) on success, (False, None) on failure.
    tweet_data will contain 'id', 'text', 'url', 'media' list (relative paths).
    """
    client_v2 = get_twitter_client_v2()
    api_v1_1 = get_twitter_api_v1_1()  # For media upload

    full_tweet_text = tweet_text

    media_ids = []
    media_relative_urls = []  # For website JSON (gh-pages paths)
    
    # Only attempt to upload images if image_paths is provided and not empty
    if image_paths and len(image_paths) > 0:
        uploaded_media_ids, uploaded_relative_urls = upload_and_attach_images(api_v1_1, image_paths)
        if uploaded_media_ids:
            media_ids = uploaded_media_ids
            media_relative_urls = uploaded_relative_urls
            logging.info(f"Attached {len(media_ids)} images to tweet.")
        else:
            logging.warning("Image upload failed, publishing tweet without images.")
    else:
        logging.debug("No valid image paths provided or image library not active, publishing tweet without images.")

    try:
        # Publish the main tweet
        if media_ids:  # Attach media_ids only if actual images were uploaded
            response = client_v2.create_tweet(text=full_tweet_text, media_ids=media_ids)
        else:
            response = client_v2.create_tweet(text=full_tweet_text)

        if response.data:
            tweet_id = response.data['id']
            bot_username = get_bot_username()  # Use the cached/fetched username
            tweet_web_url = f"https://twitter.com/{bot_username}/status/{tweet_id}"
            logging.info(f"Main tweet published: {tweet_web_url}")

            # Publish the URL as a reply to the main tweet
            reply_text = f"Source: {article_url}"
            client_v2.create_tweet(text=reply_text, in_reply_to_tweet_id=tweet_id)
            logging.info(f"Reply tweet with URL published: {article_url}")

            tweet_data = {
                'id': tweet_id,
                'text': full_tweet_text,
                'url': tweet_web_url,
                'media': media_relative_urls,  # Store relative paths for gh-pages
                'timestamp': datetime.now().isoformat()
            }
            return True, tweet_data
        else:
            logging.error(f"Failed to publish main tweet. Response: {response}")
            return False, None

    except tweepy.TweepyException as e:
        logging.error(f"Twitter API Error during tweet publishing: {e}")
        return False, None
    except Exception as e:
        logging.error(f"An unexpected error occurred during tweet publishing: {e}")
        return False, None
