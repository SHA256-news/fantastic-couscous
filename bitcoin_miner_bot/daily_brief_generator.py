# daily_brief_generator.py
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

GEMINI_MODEL = 'gemini-pro'


def generate_daily_brief(articles: List[Dict], date: str) -> str:
    """
    Generate a comprehensive daily brief from a list of articles.
    
    Args:
        articles: List of article dictionaries with title, summary, url, etc.
        date: Date string for the brief
        
    Returns:
        Markdown-formatted daily brief
    """
    if not articles:
        return f"# Bitcoin Mining Daily Brief - {date}\n\nNo articles to report today."
    
    # Prepare article summaries for Gemini
    articles_text = ""
    for i, article in enumerate(articles, 1):
        articles_text += f"\n## Article {i}\n"
        articles_text += f"**Title:** {article.get('title', 'N/A')}\n"
        articles_text += f"**Source:** {article.get('source', 'N/A')}\n"
        articles_text += f"**URL:** {article.get('url', 'N/A')}\n"
        articles_text += f"**Summary:** {article.get('summary', 'N/A')}\n"
        articles_text += f"**Content Preview:** {article.get('full_text', '')[:1000]}\n"
        articles_text += "---\n"
    
    prompt = f"""
    You are a professional Bitcoin mining news analyst. Generate a comprehensive daily brief for {date} based on the following articles.

    **Your Task:**
    1. Create an executive summary highlighting the most important developments in Bitcoin mining today
    2. Organize the brief into thematic sections (e.g., "Mining Operations", "Market Analysis", "Technology & Infrastructure", "Regulatory Updates")
    3. For each section, synthesize key insights from relevant articles
    4. Include specific data points, company names, and numbers where available
    5. Maintain a professional, objective tone
    6. Focus exclusively on Bitcoin mining - do not mention other cryptocurrencies unless directly relevant to Bitcoin mining context
    7. End with a "Looking Ahead" section summarizing implications and trends

    **Articles to analyze:**
    {articles_text[:20000]}  # Truncate to fit context window

    **Format:**
    Use Markdown formatting with clear headers, bullet points, and bold text for emphasis.
    Include article sources as inline links where appropriate.

    Generate the daily brief now:
    """
    
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        if response and response.candidates and response.candidates[0].content.parts:
            brief_content = response.candidates[0].content.parts[0].text.strip()
            
            # Add header and footer
            full_brief = f"# Bitcoin Mining Daily Brief\n"
            full_brief += f"**Date:** {date}\n"
            full_brief += f"**Articles Analyzed:** {len(articles)}\n\n"
            full_brief += "---\n\n"
            full_brief += brief_content
            full_brief += "\n\n---\n\n"
            full_brief += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
            
            return full_brief
        else:
            return f"# Bitcoin Mining Daily Brief - {date}\n\nError: Could not generate brief content."
            
    except Exception as e:
        print(f"DEBUG: Error generating daily brief: {e}")
        return f"# Bitcoin Mining Daily Brief - {date}\n\nError generating brief: {str(e)}"


def collect_articles_for_brief(state: Dict) -> List[Dict]:
    """
    Collect articles for the daily brief from state.
    
    Args:
        state: Bot state dictionary
        
    Returns:
        List of articles for the brief
    """
    # Return all articles collected for today's brief
    return state.get('daily_brief_articles', [])


def should_generate_brief(state: Dict) -> bool:
    """
    Determine if it's time to generate a daily brief.
    
    Args:
        state: Bot state dictionary
        
    Returns:
        True if brief should be generated, False otherwise
    """
    today = datetime.now().strftime('%Y-%m-%d')
    last_brief_date = state.get('last_brief_date')
    
    # Generate if we haven't generated a brief today
    if last_brief_date != today:
        # Check if we have enough articles (at least 5)
        articles = state.get('daily_brief_articles', [])
        if len(articles) >= 5:
            return True
    
    return False
