"""
Daily Brief Generator Module

Generates comprehensive daily briefs of Bitcoin mining news:
- Aggregates daily articles
- Identifies trends and themes
- Creates formatted HTML briefs
- Manages brief archive
"""

import os
import logging
import json
from datetime import datetime
from pathlib import Path
import markdown

from gemini_interface import GeminiInterface

logger = logging.getLogger(__name__)


class DailyBriefGenerator:
    """Generate daily news briefs."""
    
    def __init__(self, gemini_interface=None):
        """
        Initialize daily brief generator.
        
        Args:
            gemini_interface: Optional GeminiInterface instance
        """
        self.gemini = gemini_interface or GeminiInterface()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.gh_pages_dir = os.path.join(self.base_dir, 'gh-pages')
        self.briefs_dir = os.path.join(self.gh_pages_dir, 'briefs')
        self.template_path = os.path.join(self.gh_pages_dir, 'brief_template.html')
        
        # Ensure directories exist
        os.makedirs(self.briefs_dir, exist_ok=True)
        
        logger.info("DailyBriefGenerator initialized")
    
    def generate_brief(self, articles, date=None):
        """
        Generate a daily brief from articles.
        
        Args:
            articles: List of article dictionaries
            date: Optional date string (YYYY-MM-DD), defaults to today
            
        Returns:
            Dictionary with brief metadata
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"Generating daily brief for {date} with {len(articles)} articles")
        
        try:
            # Identify trends using Gemini
            trends = self.gemini.identify_trends(articles)
            
            # Generate brief content using Gemini
            brief_content = self.gemini.generate_brief_content(articles, trends)
            
            # Create brief metadata
            brief_meta = {
                'date': date,
                'headline': brief_content.get('headline', 'Bitcoin Mining Daily Brief'),
                'summary': brief_content.get('summary', ''),
                'article_count': len(articles),
                'trends': trends,
                'generated_at': datetime.now().isoformat()
            }
            
            # Generate HTML
            html_content = self._generate_html(brief_meta, brief_content, articles)
            
            # Save brief
            brief_filename = f"brief_{date}.html"
            brief_path = os.path.join(self.briefs_dir, brief_filename)
            
            with open(brief_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Brief saved: {brief_path}")
            
            # Update brief metadata
            brief_meta['filename'] = brief_filename
            brief_meta['url'] = f"briefs/{brief_filename}"
            
            return brief_meta
            
        except Exception as e:
            logger.error(f"Error generating brief: {e}", exc_info=True)
            return None
    
    def _generate_html(self, brief_meta, brief_content, articles):
        """
        Generate HTML for the brief.
        
        Args:
            brief_meta: Brief metadata dictionary
            brief_content: Brief content from Gemini
            articles: List of articles
            
        Returns:
            HTML string
        """
        # Try to load template
        template = self._load_template()
        
        if template:
            # Replace template placeholders
            html = template
            html = html.replace('{{DATE}}', brief_meta['date'])
            html = html.replace('{{HEADLINE}}', brief_meta['headline'])
            html = html.replace('{{SUMMARY}}', brief_meta['summary'])
            html = html.replace('{{CONTENT}}', self._format_brief_content(brief_content, articles))
        else:
            # Generate HTML without template
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{brief_meta['headline']}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .brief {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{
            border-bottom: 3px solid #f7931a;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .date {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 10px;
        }}
        h1 {{
            color: #333;
            margin: 10px 0;
        }}
        .summary {{
            font-size: 1.1em;
            color: #555;
            font-style: italic;
            margin: 20px 0;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #f7931a;
        }}
        .section {{
            margin: 30px 0;
        }}
        .section h2 {{
            color: #f7931a;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        .article {{
            margin: 15px 0;
            padding: 15px;
            background: #fafafa;
            border-radius: 4px;
        }}
        .article h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .article a {{
            color: #f7931a;
            text-decoration: none;
        }}
        .article a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="brief">
        <div class="header">
            <div class="date">{brief_meta['date']}</div>
            <h1>{brief_meta['headline']}</h1>
        </div>
        
        <div class="summary">
            {brief_meta['summary']}
        </div>
        
        {self._format_brief_content(brief_content, articles)}
        
        <div class="footer">
            Generated by SHA256.news Bitcoin Mining Bot<br>
            <a href="../index.html">← Back to Home</a>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _format_brief_content(self, brief_content, articles):
        """
        Format brief content into HTML.
        
        Args:
            brief_content: Content dictionary from Gemini
            articles: List of articles
            
        Returns:
            HTML string
        """
        html_parts = []
        
        # Add sections from Gemini
        sections = brief_content.get('sections', [])
        for section in sections:
            title = section.get('title', '')
            content = section.get('content', '')
            
            html_parts.append(f"""
        <div class="section">
            <h2>{title}</h2>
            <p>{content}</p>
        </div>""")
        
        # Add article list
        if articles:
            html_parts.append("""
        <div class="section">
            <h2>Featured Articles</h2>""")
            
            for article in articles[:10]:  # Top 10 articles
                title = article.get('title', 'Untitled')
                url = article.get('url', '#')
                summary = article.get('ai_summary', article.get('body', ''))[:200]
                source = article.get('source', 'Unknown Source')
                
                html_parts.append(f"""
            <div class="article">
                <h3><a href="{url}" target="_blank">{title}</a></h3>
                <p>{summary}...</p>
                <small>Source: {source}</small>
            </div>""")
            
            html_parts.append("""
        </div>""")
        
        return '\n'.join(html_parts)
    
    def _load_template(self):
        """
        Load HTML template if available.
        
        Returns:
            Template string or None
        """
        try:
            if os.path.exists(self.template_path):
                with open(self.template_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            logger.warning(f"Could not load template: {e}")
        
        return None
    
    def get_recent_briefs(self, limit=10):
        """
        Get metadata for recent briefs.
        
        Args:
            limit: Maximum number of briefs to return
            
        Returns:
            List of brief metadata dictionaries
        """
        briefs = []
        
        try:
            if not os.path.exists(self.briefs_dir):
                return briefs
            
            # Get all brief files
            brief_files = sorted(
                [f for f in os.listdir(self.briefs_dir) if f.startswith('brief_') and f.endswith('.html')],
                reverse=True
            )
            
            for filename in brief_files[:limit]:
                # Extract date from filename
                date_str = filename.replace('brief_', '').replace('.html', '')
                
                briefs.append({
                    'date': date_str,
                    'filename': filename,
                    'url': f"briefs/{filename}",
                    'title': f"Brief for {date_str}"
                })
            
            logger.info(f"Found {len(briefs)} recent briefs")
            
        except Exception as e:
            logger.error(f"Error getting recent briefs: {e}", exc_info=True)
        
        return briefs
