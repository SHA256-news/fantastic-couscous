# image_manager.py
import os
import random
import re
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()

# Base directories for images
IMAGE_DIR = "images"
COMPANY_LOGOS_DIR = os.path.join(IMAGE_DIR, "company_logos")
CONCEPTUAL_IMAGES_DIR = os.path.join(IMAGE_DIR, "conceptual")

# Image Library Activation Flag
# Read from .env, defaults to False if not set or invalid (via GitHub Secrets in production)
IMAGE_LIBRARY_ACTIVE = os.getenv("IMAGE_LIBRARY_ACTIVE", "False").lower() == "true"
if not IMAGE_LIBRARY_ACTIVE:
    logging.info("Image library is currently INACTIVE. No images will be attached to tweets.")


# Placeholder for a mapping of company names to their logo filenames
# This dictionary will be populated and maintained manually or via automation later
COMPANY_LOGO_MAP = {
    "riot platforms": "riot_platforms.png",
    "marathon digital": "marathon_digital.png",
    "cleanspark": "cleanspark.png",
    "bitfarms": "bitfarms.png",
    "iris energy": "iris_energy.png",
    "hive digital": "hive_digital.png",
    "galaxy digital": "galaxy_digital.png",
    "argo blockchain": "argo_blockchain.png",
    # Add more mappings as you build your library
}

def get_company_logo_path(company_name: str) -> str | None:
    """
    Attempts to find a local company logo based on the company name.
    Performs case-insensitive matching and checks for file existence.
    """
    normalized_name = company_name.lower().strip()
    filename = COMPANY_LOGO_MAP.get(normalized_name)
    if filename:
        path = os.path.join(COMPANY_LOGOS_DIR, filename)
        if os.path.exists(path):
            logging.debug(f"Found company logo for '{company_name}' at {path}.")
            return path
        else:
            logging.debug(f"Company logo file not found for '{company_name}' at {path}.")
    return None

def get_random_conceptual_image_path() -> str | None:
    """
    Selects a random image from the conceptual images directory.
    Checks for file existence.
    """
    if not os.path.exists(CONCEPTUAL_IMAGES_DIR):
        logging.warning(f"Conceptual images directory not found: {CONCEPTUAL_IMAGES_DIR}")
        return None

    valid_images = [
        f for f in os.listdir(CONCEPTUAL_IMAGES_DIR)
        if os.path.isfile(os.path.join(CONCEPTUAL_IMAGES_DIR, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]

    if valid_images:
        selected_file = random.choice(valid_images)
        logging.debug(f"Selected random conceptual image: {selected_file}")
        return os.path.join(CONCEPTUAL_IMAGES_DIR, selected_file)
    else:
        logging.warning(f"No valid conceptual images found in {CONCEPTUAL_IMAGES_DIR}.")
        return None

def extract_company_name_from_tweet_text(tweet_text: str) -> str | None:
    """
    Tries to extract a company name from the tweet text to aid in image selection.
    This is a simple heuristic and can be improved.
    """
    # Look for common Bitcoin mining company names first (full phrases)
    common_miners = list(COMPANY_LOGO_MAP.keys()) # Use keys from your map
    for miner in sorted(common_miners, key=len, reverse=True): # Check longer names first
        if miner in tweet_text.lower():
            logging.debug(f"Extracted company name hint: '{miner}' from tweet text.")
            return miner

    # A more generic approach: look for capitalized words that might be companies
    # Exclude common stop words if they appear capitalized
    stop_words = {"A", "An", "The", "In", "On", "At", "By", "For", "With", "Of", "And", "Or", "But", "Is", "Are", "Was", "Were", "Be", "Been", "Being"}
    
    # Matches capitalized phrases that are likely proper nouns
    matches = re.findall(r'\b[A-Z][a-zA-Z]* (?:\b[A-Z][a-zA-Z]*)*\b', tweet_text)
    
    # Filter out single stop words or phrases composed entirely of stop words, and too short words
    matches = [m for m in matches if m.lower() not in stop_words and len(m) > 3]
    
    if matches:
        # Prioritize longest matches, assuming they are more specific company names
        longest_match = max(matches, key=len)
        logging.debug(f"Extracted generic company name hint: '{longest_match}' from tweet text.")
        return longest_match
    
    logging.debug("No company name hint extracted from tweet text.")
    return None


def select_images_for_tweet(tweet_text: str) -> list[str]:
    """
    Selects image paths for a tweet.
    Includes a company logo (if identifiable) and one random conceptual image (if active).
    Returns an empty list if IMAGE_LIBRARY_ACTIVE is False.
    """
    if not IMAGE_LIBRARY_ACTIVE:
        logging.info("Image library inactive, returning empty list for images.")
        return []

    selected_image_paths = []

    # 1. Try to find a company logo
    company_name_hint = extract_company_name_from_tweet_text(tweet_text)
    if company_name_hint:
        logo_path = get_company_logo_path(company_name_hint)
        if logo_path:
            selected_image_paths.append(logo_path)
            logging.info(f"Selected company logo for tweet: {logo_path}")
            
    # 2. Try to get one random conceptual image (if we still need an image)
    if len(selected_image_paths) < 2:
        conceptual_image_path = get_random_conceptual_image_path()
        if conceptual_image_path:
            # Ensure conceptual image is not already the company logo (unlikely, but safe)
            if conceptual_image_path not in selected_image_paths:
                selected_image_paths.append(conceptual_image_path)
                logging.info(f"Selected conceptual image for tweet: {conceptual_image_path}")

    # Limit to maximum 2 images for Twitter
    final_selection = selected_image_paths[:2]
    logging.info(f"Final image selection for tweet: {final_selection}")
    return final_selection


def ensure_placeholder_images():
    """
    Creates placeholder images if they don't exist.
    This is called during bot initialization to ensure basic conceptual images are available.
    """
    # Create a simple 1x1 pixel PNG as placeholder
    # In a real implementation, these would be actual images
    placeholder_png_data = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    # Ensure directories exist
    os.makedirs(COMPANY_LOGOS_DIR, exist_ok=True)
    os.makedirs(CONCEPTUAL_IMAGES_DIR, exist_ok=True)
    
    # Create placeholder conceptual images if they don't exist
    # Check for any image files with supported extensions
    existing_images = [
        f for f in os.listdir(CONCEPTUAL_IMAGES_DIR)
        if os.path.isfile(os.path.join(CONCEPTUAL_IMAGES_DIR, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ] if os.path.exists(CONCEPTUAL_IMAGES_DIR) else []
    
    # If no images exist, create basic placeholders
    if not existing_images:
        placeholder_files = ["bitcoin_logo.png", "default_mining_concept.png", "mining_farm_generic.png"]
        for img_file in placeholder_files:
            img_path = os.path.join(CONCEPTUAL_IMAGES_DIR, img_file)
            if not os.path.exists(img_path):
                try:
                    with open(img_path, 'wb') as f:
                        f.write(placeholder_png_data)
                    logging.info(f"Created placeholder image: {img_path}")
                except Exception as e:
                    logging.warning(f"Could not create placeholder image {img_path}: {e}")
    
    logging.info("Image placeholders ensured.")
