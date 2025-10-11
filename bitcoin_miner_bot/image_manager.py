"""
Image Manager Module

Handles intelligent image selection for tweets:
- Company logo matching
- Conceptual image selection
- Image fallback logic
"""

import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageManager:
    """Manage and select appropriate images for content."""
    
    def __init__(self):
        """Initialize image manager."""
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.images_dir = os.path.join(self.base_dir, 'images')
        self.company_logos_dir = os.path.join(self.images_dir, 'company_logos')
        self.conceptual_dir = os.path.join(self.images_dir, 'conceptual')
        
        # Known company name to logo mappings
        self.company_mappings = {
            'bitmain': 'bitmain.png',
            'antminer': 'bitmain.png',
            'microbt': 'microbt.png',
            'whatsminer': 'microbt.png',
            'riot': 'riot.png',
            'riot platforms': 'riot.png',
            'marathon': 'marathon.png',
            'marathon digital': 'marathon.png',
            'core scientific': 'core_scientific.png',
            'hut 8': 'hut8.png',
            'hut8': 'hut8.png',
            'cleanspark': 'cleanspark.png',
            'bitfarms': 'bitfarms.png',
            'canaan': 'canaan.png',
            'avalon': 'canaan.png',
            'foundry': 'foundry.png',
            'luxor': 'luxor.png',
            'f2pool': 'f2pool.png',
            'antpool': 'antpool.png',
            'btc.com': 'btccom.png'
        }
        
        # Conceptual images for different topics
        self.topic_images = {
            'hashrate': 'default_mining_concept.png',
            'difficulty': 'default_mining_concept.png',
            'hardware': 'default_mining_concept.png',
            'mining farm': 'mining_farm_generic.png',
            'bitcoin': 'bitcoin_logo.png',
            'default': 'bitcoin_logo.png'
        }
        
        logger.info("ImageManager initialized")
    
    def select_image(self, article):
        """
        Select the most appropriate image for an article.
        
        Args:
            article: Article dictionary with title, body, etc.
            
        Returns:
            Path to selected image file or None
        """
        # Priority 1: Check for company logos
        company_logo = self._find_company_logo(article)
        if company_logo and os.path.exists(company_logo):
            logger.info(f"Selected company logo: {company_logo}")
            return company_logo
        
        # Priority 2: Check for topic-based conceptual image
        conceptual_image = self._find_conceptual_image(article)
        if conceptual_image and os.path.exists(conceptual_image):
            logger.info(f"Selected conceptual image: {conceptual_image}")
            return conceptual_image
        
        # Priority 3: Use default Bitcoin logo
        default_image = os.path.join(self.conceptual_dir, 'bitcoin_logo.png')
        if os.path.exists(default_image):
            logger.info(f"Using default image: {default_image}")
            return default_image
        
        logger.warning("No suitable image found")
        return None
    
    def _find_company_logo(self, article):
        """
        Find appropriate company logo based on article content.
        
        Args:
            article: Article dictionary
            
        Returns:
            Path to company logo or None
        """
        text = (article.get('title', '') + ' ' + article.get('body', '')).lower()
        
        # Check each company mapping
        for company_name, logo_filename in self.company_mappings.items():
            if company_name.lower() in text:
                logo_path = os.path.join(self.company_logos_dir, logo_filename)
                if os.path.exists(logo_path):
                    logger.debug(f"Found company match: {company_name} -> {logo_filename}")
                    return logo_path
        
        return None
    
    def _find_conceptual_image(self, article):
        """
        Find appropriate conceptual image based on article topics.
        
        Args:
            article: Article dictionary
            
        Returns:
            Path to conceptual image or None
        """
        text = (article.get('title', '') + ' ' + article.get('body', '')).lower()
        
        # Check for topic keywords
        for topic, image_filename in self.topic_images.items():
            if topic in text:
                image_path = os.path.join(self.conceptual_dir, image_filename)
                if os.path.exists(image_path):
                    logger.debug(f"Found topic match: {topic} -> {image_filename}")
                    return image_path
        
        return None
    
    def list_available_images(self):
        """
        List all available images.
        
        Returns:
            Dictionary with image categories and file lists
        """
        available = {
            'company_logos': [],
            'conceptual': []
        }
        
        # List company logos
        if os.path.exists(self.company_logos_dir):
            available['company_logos'] = [
                f for f in os.listdir(self.company_logos_dir)
                if f.endswith(('.png', '.jpg', '.jpeg'))
            ]
        
        # List conceptual images
        if os.path.exists(self.conceptual_dir):
            available['conceptual'] = [
                f for f in os.listdir(self.conceptual_dir)
                if f.endswith(('.png', '.jpg', '.jpeg'))
            ]
        
        logger.info(f"Available images: {len(available['company_logos'])} logos, "
                   f"{len(available['conceptual'])} conceptual")
        
        return available
    
    def add_company_logo(self, company_name, logo_path):
        """
        Add a new company logo to the collection.
        
        Args:
            company_name: Company name key
            logo_path: Path to logo file to copy
            
        Returns:
            Boolean success status
        """
        try:
            import shutil
            
            if not os.path.exists(logo_path):
                logger.error(f"Logo file not found: {logo_path}")
                return False
            
            # Create company logos directory if it doesn't exist
            os.makedirs(self.company_logos_dir, exist_ok=True)
            
            # Generate filename
            filename = f"{company_name.lower().replace(' ', '_')}.png"
            dest_path = os.path.join(self.company_logos_dir, filename)
            
            # Copy file
            shutil.copy2(logo_path, dest_path)
            
            logger.info(f"Added company logo: {company_name} -> {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding company logo: {e}", exc_info=True)
            return False
