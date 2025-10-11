"""
Gemini AI Interface Module

Handles all interactions with Google's Gemini AI:
- Article enhancement and summarization
- Tweet content generation
- Search query generation
- Daily brief generation with thematic trend identification
"""

import os
import logging
import json
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiInterface:
    """Interface for Google Gemini AI interactions."""
    
    def __init__(self):
        """Initialize Gemini interface."""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not set, AI features will be limited")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini interface initialized")
    
    def enhance_article(self, article):
        """
        Enhance article with AI-generated insights.
        
        Args:
            article: Article dictionary
            
        Returns:
            Enhanced article dictionary
        """
        if not self.model:
            logger.warning("Gemini not configured, returning article without enhancement")
            return article
        
        try:
            title = article.get('title', '')
            body = article.get('body', '')[:2000]  # Limit input
            
            prompt = f"""Analyze this Bitcoin mining news article and provide:
1. A concise summary (2-3 sentences)
2. Key topics/themes (comma-separated)
3. Sentiment (positive/neutral/negative)
4. Significance score (1-10)

Article Title: {title}
Article Content: {body}

Respond in JSON format:
{{
  "summary": "...",
  "topics": ["topic1", "topic2", ...],
  "sentiment": "...",
  "significance": X
}}"""
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            try:
                enhancement = json.loads(response.text)
                article['ai_summary'] = enhancement.get('summary', '')
                article['ai_topics'] = enhancement.get('topics', [])
                article['ai_sentiment'] = enhancement.get('sentiment', 'neutral')
                article['ai_significance'] = enhancement.get('significance', 5)
                logger.info(f"Enhanced article: {title}")
            except json.JSONDecodeError:
                logger.warning("Could not parse Gemini JSON response")
                article['ai_summary'] = response.text[:500]
            
        except Exception as e:
            logger.error(f"Error enhancing article: {e}", exc_info=True)
        
        return article
    
    def generate_tweet_content(self, article):
        """
        Generate engaging tweet content for an article.
        
        Args:
            article: Article dictionary
            
        Returns:
            Tweet text string
        """
        if not self.model:
            # Fallback: simple tweet generation
            title = article.get('title', '')
            url = article.get('url', '')
            return f"🔶 {title[:200]} {url}"
        
        try:
            title = article.get('title', '')
            summary = article.get('ai_summary', article.get('body', ''))[:500]
            
            prompt = f"""Create an engaging, informative tweet about this Bitcoin mining news.

Article Title: {title}
Summary: {summary}

Requirements:
- Maximum 240 characters (leave room for URL)
- Include relevant emoji (mining/bitcoin themed)
- Be professional and informative
- Highlight the most newsworthy aspect
- Don't include URL (it will be added automatically)

Tweet:"""
            
            response = self.model.generate_content(prompt)
            tweet_text = response.text.strip()
            
            # Ensure it fits with URL
            if len(tweet_text) > 240:
                tweet_text = tweet_text[:237] + "..."
            
            logger.info(f"Generated tweet: {tweet_text[:50]}...")
            return tweet_text
            
        except Exception as e:
            logger.error(f"Error generating tweet: {e}", exc_info=True)
            # Fallback
            title = article.get('title', '')
            return f"🔶 {title[:240]}"
    
    def generate_search_queries(self, trend_analysis=None):
        """
        Generate optimized search queries for Bitcoin mining news.
        
        Args:
            trend_analysis: Optional previous trend analysis for context
            
        Returns:
            List of search query strings
        """
        if not self.model:
            # Default queries
            return [
                "bitcoin mining",
                "cryptocurrency mining hardware",
                "bitcoin hashrate news"
            ]
        
        try:
            context = ""
            if trend_analysis:
                context = f"Recent trends: {trend_analysis}"
            
            prompt = f"""Generate 5 specific, targeted search queries for finding the latest Bitcoin mining news.

{context}

Focus on:
- Mining hardware and technology
- Mining companies and operations
- Hashrate and difficulty changes
- Mining economics and profitability
- Regulatory news affecting mining

Return as JSON array: ["query1", "query2", ...]"""
            
            response = self.model.generate_content(prompt)
            
            try:
                queries = json.loads(response.text)
                logger.info(f"Generated {len(queries)} search queries")
                return queries
            except json.JSONDecodeError:
                logger.warning("Could not parse search queries JSON")
                return ["bitcoin mining", "mining hardware", "hashrate news"]
            
        except Exception as e:
            logger.error(f"Error generating search queries: {e}", exc_info=True)
            return ["bitcoin mining", "mining hardware", "hashrate news"]
    
    def identify_trends(self, articles):
        """
        Identify thematic trends from a collection of articles.
        
        Args:
            articles: List of article dictionaries
            
        Returns:
            Dictionary with trend analysis
        """
        if not self.model or not articles:
            return {
                'themes': [],
                'summary': 'No trend analysis available',
                'key_developments': []
            }
        
        try:
            # Prepare article summaries
            article_texts = []
            for article in articles[:20]:  # Limit to 20 articles
                title = article.get('title', '')
                summary = article.get('ai_summary', article.get('body', ''))[:200]
                article_texts.append(f"- {title}: {summary}")
            
            articles_text = "\n".join(article_texts)
            
            prompt = f"""Analyze these Bitcoin mining news articles and identify:
1. Major themes/topics (3-5)
2. Overall trend summary (2-3 sentences)
3. Key developments (3-5 bullet points)

Articles:
{articles_text}

Respond in JSON format:
{{
  "themes": ["theme1", "theme2", ...],
  "summary": "...",
  "key_developments": ["dev1", "dev2", ...]
}}"""
            
            response = self.model.generate_content(prompt)
            
            try:
                trends = json.loads(response.text)
                logger.info(f"Identified {len(trends.get('themes', []))} themes")
                return trends
            except json.JSONDecodeError:
                logger.warning("Could not parse trends JSON")
                return {
                    'themes': ['mining', 'technology', 'market'],
                    'summary': response.text[:500],
                    'key_developments': []
                }
            
        except Exception as e:
            logger.error(f"Error identifying trends: {e}", exc_info=True)
            return {
                'themes': [],
                'summary': 'Error analyzing trends',
                'key_developments': []
            }
    
    def generate_brief_content(self, articles, trends):
        """
        Generate daily brief content from articles and trends.
        
        Args:
            articles: List of article dictionaries
            trends: Trend analysis dictionary
            
        Returns:
            Dictionary with brief content
        """
        if not self.model:
            # Simple fallback brief
            return {
                'headline': 'Bitcoin Mining Daily Brief',
                'summary': 'Latest Bitcoin mining news and developments.',
                'sections': []
            }
        
        try:
            # Prepare context
            trend_summary = trends.get('summary', '')
            themes = ', '.join(trends.get('themes', []))
            
            article_list = []
            for i, article in enumerate(articles[:10], 1):
                title = article.get('title', '')
                summary = article.get('ai_summary', '')[:150]
                article_list.append(f"{i}. {title}: {summary}")
            
            articles_text = "\n".join(article_list)
            
            prompt = f"""Create a professional daily brief for Bitcoin mining news.

Current Trends: {trend_summary}
Key Themes: {themes}

Top Articles:
{articles_text}

Create a brief with:
1. Compelling headline
2. Executive summary (3-4 sentences)
3. 3-5 themed sections with analysis

Respond in JSON format:
{{
  "headline": "...",
  "summary": "...",
  "sections": [
    {{
      "title": "Section Title",
      "content": "Section content..."
    }},
    ...
  ]
}}"""
            
            response = self.model.generate_content(prompt)
            
            try:
                brief = json.loads(response.text)
                logger.info("Generated daily brief")
                return brief
            except json.JSONDecodeError:
                logger.warning("Could not parse brief JSON")
                return {
                    'headline': 'Bitcoin Mining Daily Brief',
                    'summary': response.text[:500],
                    'sections': []
                }
            
        except Exception as e:
            logger.error(f"Error generating brief: {e}", exc_info=True)
            return {
                'headline': 'Bitcoin Mining Daily Brief',
                'summary': 'Error generating brief',
                'sections': []
            }
