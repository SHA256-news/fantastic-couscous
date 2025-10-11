# image_manager.py
import os
from typing import Optional

# Base directory for images
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'images')
COMPANY_LOGOS_DIR = os.path.join(IMAGES_DIR, 'company_logos')

# Default images
DEFAULT_BITCOIN_LOGO = os.path.join(IMAGES_DIR, 'bitcoin_logo.png')
DEFAULT_MINING_CONCEPT = os.path.join(IMAGES_DIR, 'default_mining_concept.png')

# Company name to logo file mapping
COMPANY_LOGO_MAP = {
    'riot platforms': 'riot_platforms.png',
    'marathon digital': 'marathon_digital.png',
    'cleanspark': 'cleanspark.png',
    'bitfarms': 'bitfarms.png',
    'iris energy': 'iris_energy.png',
    'hive digital': 'hive_digital.png',
    'core scientific': 'core_scientific.png',
    'hut 8': 'hut_8.png',
    'cipher mining': 'cipher_mining.png',
    'terawulf': 'terawulf.png'
}


def get_image_for_article(article_title: str, article_content: str) -> Optional[str]:
    """
    Determines the appropriate image for an article based on its content.
    
    Args:
        article_title: The article title
        article_content: The article content
        
    Returns:
        Path to the image file, or None if no suitable image found
    """
    # Combine title and content for analysis
    combined_text = f"{article_title} {article_content}".lower()
    
    # Check for company mentions
    for company_name, logo_filename in COMPANY_LOGO_MAP.items():
        if company_name in combined_text:
            logo_path = os.path.join(COMPANY_LOGOS_DIR, logo_filename)
            if os.path.exists(logo_path):
                return logo_path
    
    # Default to mining concept image if it exists
    if os.path.exists(DEFAULT_MINING_CONCEPT):
        return DEFAULT_MINING_CONCEPT
    
    # Fall back to Bitcoin logo if it exists
    if os.path.exists(DEFAULT_BITCOIN_LOGO):
        return DEFAULT_BITCOIN_LOGO
    
    # No image found
    return None


def ensure_placeholder_images():
    """
    Creates placeholder image files if they don't exist.
    This is a minimal implementation that creates dummy files.
    In production, these should be replaced with actual images.
    """
    # Ensure directories exist
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(COMPANY_LOGOS_DIR, exist_ok=True)
    
    # Create placeholder files if they don't exist
    placeholder_files = [
        DEFAULT_BITCOIN_LOGO,
        DEFAULT_MINING_CONCEPT
    ]
    
    for filepath in placeholder_files:
        if not os.path.exists(filepath):
            # Create a minimal PNG file (1x1 transparent pixel)
            # This is a valid PNG file in bytes
            png_data = (
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
                b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
                b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
            )
            with open(filepath, 'wb') as f:
                f.write(png_data)
            print(f"DEBUG: Created placeholder image: {filepath}")
