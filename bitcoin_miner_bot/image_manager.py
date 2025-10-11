# image_manager.py
import os
import logging
import random
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Image library activation flag from environment
IMAGE_LIBRARY_ACTIVE = os.getenv("IMAGE_LIBRARY_ACTIVE", "False").lower() == "true"

# Base paths for image directories (relative to project root)
COMPANY_LOGOS_DIR = "images/company_logos"
CONCEPTUAL_DIR = "images/conceptual"

# Company name to logo file mapping
COMPANY_LOGO_MAP = {
    "riot": "riot_logo.png",
    "riot platforms": "riot_logo.png",
    "marathon": "marathon_logo.png",
    "marathon digital": "marathon_logo.png",
    "cleanspark": "cleanspark_logo.png",
    "bitfarms": "bitfarms_logo.png",
    "iris energy": "iris_energy_logo.png",
    "hive": "hive_logo.png",
    "hive digital": "hive_logo.png",
    "hut 8": "hut8_logo.png",
    "cipher mining": "cipher_mining_logo.png",
    "terawulf": "terawulf_logo.png",
    "core scientific": "core_scientific_logo.png",
}

# Conceptual fallback images
CONCEPTUAL_IMAGES = [
    "bitcoin_logo.png",
    "default_mining_concept.png",
    "mining_farm_generic.png"
]


def get_image_for_article(article_title: str, article_content: str, source_title: str) -> Optional[List[str]]:
    """
    Determines appropriate image(s) for an article based on content.
    Returns a list of image paths (relative to project root) or None if no images should be attached.
    
    Logic:
    1. If IMAGE_LIBRARY_ACTIVE is False, return None (no images)
    2. Check if article mentions specific companies, use company logo if available
    3. Otherwise, randomly select from conceptual images
    """
    if not IMAGE_LIBRARY_ACTIVE:
        logging.debug("Image library is not active. No images will be attached.")
        return None
    
    # Combine title and content for matching (convert to lowercase for case-insensitive matching)
    combined_text = (article_title + " " + article_content + " " + source_title).lower()
    
    # Check for company mentions
    for company_name, logo_file in COMPANY_LOGO_MAP.items():
        if company_name in combined_text:
            logo_path = os.path.join(COMPANY_LOGOS_DIR, logo_file)
            if os.path.exists(logo_path):
                logging.info(f"Found company logo for '{company_name}': {logo_path}")
                return [logo_path]
            else:
                logging.debug(f"Logo file not found: {logo_path}")
    
    # Fallback to conceptual images
    available_conceptual = []
    for img_file in CONCEPTUAL_IMAGES:
        img_path = os.path.join(CONCEPTUAL_DIR, img_file)
        if os.path.exists(img_path):
            available_conceptual.append(img_path)
    
    if available_conceptual:
        selected_image = random.choice(available_conceptual)
        logging.info(f"Using conceptual image: {selected_image}")
        return [selected_image]
    else:
        logging.warning("No conceptual images found. Tweet will be published without images.")
        return None


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
    os.makedirs(CONCEPTUAL_DIR, exist_ok=True)
    
    # Create placeholder conceptual images if they don't exist
    for img_file in CONCEPTUAL_IMAGES:
        img_path = os.path.join(CONCEPTUAL_DIR, img_file)
        if not os.path.exists(img_path):
            try:
                with open(img_path, 'wb') as f:
                    f.write(placeholder_png_data)
                logging.info(f"Created placeholder image: {img_path}")
            except Exception as e:
                logging.warning(f"Could not create placeholder image {img_path}: {e}")
    
    logging.info("Image placeholders ensured.")
