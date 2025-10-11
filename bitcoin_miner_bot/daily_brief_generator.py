# daily_brief_generator.py
import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import re
import markdown # For Markdown to HTML conversion

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Model to use, configurable via environment variable (from .env or GitHub Secrets)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", 'gemini-pro')
logging.info(f"Using Gemini model for daily brief: {GEMINI_MODEL}")

def _robust_generate_content(prompt: str):
    """
    Helper function to safely call Gemini and extract text, handling common response structures.
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        # Robustly check for response and content structure
        if response and response.candidates:
            if len(response.candidates) > 0 and response.candidates[0].content and len(response.candidates[0].content.parts) > 0:
                return response.candidates[0].content.parts[0].text
        logging.warning("Gemini response was empty or did not contain expected content parts for brief generation.")
        return None
    except Exception as e:
        logging.error(f"Error during Gemini API call for brief generation: {e}")
        return None

# Placeholder for future: This would execute actual external search API
def _execute_external_grounding_search(queries: List[str]) -> str:
    """
    Simulates executing external search queries for grounding context.
    In a real implementation, this would call Google Custom Search API, SerpAPI, etc.
    and process results. Requires API keys (e.g., GOOGLE_CUSTOM_SEARCH_API_KEY, GOOGLE_CUSTOM_SEARCH_CX).
    """
    logging.info(f"Simulating external search for grounding with queries: {queries}")
    if not queries:
        return ""
    # Example placeholder result:
    return (
        f"External search context based on: {', '.join(queries)}. "
        "Recent data indicates Bitcoin hashrate hitting new all-time highs, "
        "driven by increased efficiency of next-gen ASICs and strategic energy partnerships. "
        "Political debates in Texas and Paraguay continue to shape local energy pricing and regulatory frameworks for large-scale mining operations. "
        "ASIC supply chain remains stable with focus on 3nm/5nm process nodes for power optimization."
    )


def generate_grounding_queries_with_gemini(article_contents: List[Dict[str, Any]]) -> List[str]:
    """
    Uses Gemini to generate targeted search queries for grounding context based on article content.
    """
    # Aggregate content from the articles provided for the brief
    aggregated_content = "\n\n".join([a['full_content'][:5000] for a in article_contents if 'full_content' in a])
    if not aggregated_content:
        logging.warning("No article content available to generate grounding queries.")
        return []

    prompt = f"""
    Analyze the following aggregated Bitcoin mining article content. Based on the key themes, companies, and developments mentioned, generate 3-5 specific search queries that would provide broader context and grounding related to:
    - Energy Market (e.g., costs, sources, demand, competition)
    - Politics/Regulation (e.g., government incentives, legislative debates, local impacts)
    - ASIC Manufacturing/Hardware (e.g., market trends, repurposing challenges, supply chain)

    Each query should be concise and optimized for a web search engine. Return a comma-separated list of these queries.

    Aggregated Article Content:
    ---
    {aggregated_content}
    ---

    Example Output: Bitcoin mining energy costs, US bitcoin miner regulations, ASIC chip advancements
    """
    result = _robust_generate_content(prompt)
    if result:
        queries_str = result.strip()
        return [q.strip() for q in queries_str.split(',') if q.strip()]
    logging.error("Failed to generate grounding search queries from Gemini.")
    return []

def generate_brief_deck(brief_content_md: str) -> str:
    """
    Uses Gemini to generate a 1-2 sentence brief deck (summary) for the homepage index.
    """
    prompt = f"""
    From the following daily Bitcoin Mining brief content (Markdown format), generate a concise, 1-2 sentence summary (deck) suitable for a website's homepage or index listing.
    The summary should capture the main essence or key highlights of the brief. It should not exceed 200 characters.

    Brief Content:
    ---
    {brief_content_md[:10000]} # Limit brief content for deck generation
    ---

    Return only the 1-2 sentence summary.
    """
    result = _robust_generate_content(prompt)
    if result:
        deck = result.strip()
        if len(deck) > 200:
            deck = deck[:197] + "..." # Truncate if Gemini is too verbose
        return deck
    logging.warning("Failed to generate brief deck from Gemini, using generic fallback.")
    return "A comprehensive daily summary of key developments in the Bitcoin mining industry."

def identify_daily_themes_with_gemini(brief_content_md: str) -> List[str]:
    """
    Uses Gemini to identify 2-3 overarching themes or trends from the daily brief.
    """
    prompt = f"""
    Analyze the following daily Bitcoin Mining brief (Markdown format) and identify 2-3 overarching, significant trends or themes.
    Each theme should be a concise phrase (e.g., "Shift to AI Infrastructure", "Rising Energy Costs in Texas", "Regulatory Scrutiny in South America").
    Return a comma-separated list of these themes.

    Brief Content:
    ---
    {brief_content_md[:15000]} # Limit content for theme generation
    ---

    Example Output: Shift to AI Infrastructure, Expanding Geographies, Hashrate Growth
    """
    result = _robust_generate_content(prompt)
    if result:
        themes_str = result.strip()
        return [theme.strip() for theme in themes_str.split(',') if theme.strip()]
    logging.warning("Failed to generate thematic trends from Gemini.")
    return []


def generate_daily_brief(articles_for_brief: List[Dict[str, Any]], aggregated_grounding_context_text: str = "") -> Dict[str, str]:
    """
    Generates the full daily blog brief using Gemini, synthesizing multiple articles
    and incorporating extensive grounding context.
    Returns a dictionary containing 'brief_title', 'brief_deck', 'brief_content_md', 'brief_themes'.
    """
    if not articles_for_brief:
        logging.warning("No articles provided to generate the daily brief.")
        return {"brief_title": "ERROR: No brief generated", "brief_deck": "No content for brief.", "brief_content_md": "No content.", "brief_themes": []}

    # Extract original URL content directly from passed articles_for_brief (avoids re-fetching)
    articles_text_for_prompt = []
    for article_data in articles_for_brief:
        articles_text_for_prompt.append(f"--- ARTICLE ---\nURL: {article_data.get('url', 'N/A')}\nTitle: {article_data.get('html_title', 'N/A')}\nContent: {article_data.get('full_content', '')[:30000]}\n")
    
    all_articles_text = "\n".join(articles_text_for_prompt)

    # Combine all context for Gemini
    full_context_for_gemini = f"""
    {all_articles_text}

    --- ADDITIONAL GROUNDING CONTEXT ---
    {aggregated_grounding_context_text}
    --- END ADDITIONAL GROUNDING CONTEXT ---
    """

    prompt = f"""
    You are an expert financial journalist specializing in the Bitcoin mining industry, tasked with generating a concise, informative, and highly readable daily blog brief. This brief must synthesize the day's significant news, integrate extensive external context, and provide forward-looking insights for a sophisticated audience of Bitcoin miners.

    **Overall Theme & Tone:**
    *   **Theme:** "Today, in Bitcoin Mining: A Daily Brief" This exact phrase should be the primary title.
    *   **Tone:** Professional, analytical, and insightful, akin to the Wall Street Journal or Financial Times. The language must be direct, simple, and easy to read for individuals with a low attention span, avoiding jargon where possible or explaining it clearly.

    **Core Tenets of Ethical Journalism (Adhere strictly to all):**
    1.  **Truth and Accuracy:** Verify all information, present it in context, and clearly distinguish fact from opinion.
    2.  **Independence:** Avoid conflicts of interest or bias; serve the public's right to know without external influence.
    3.  **Fairness and Impartiality:** Present balanced accounts, avoid favoritism, and provide necessary context for all significant aspects of a story.
    4.  **Minimizing Harm:** Treat sources and subjects with respect and compassion; consider the potential consequences of publishing sensitive information.
    5.  **Accountability and Transparency:** Be transparent about the information presented and responsible for the content.

    **Content Requirements:**
    1.  **Synthesize News from Provided URLs:** Integrate key information from ALL provided URLs into a coherent, flowing narrative. These URLs represent both the day's directly covered news and broader contextual articles.
    2.  **Extensive Grounding & Context:** Beyond synthesizing the article content, leverage a deep understanding of external information (as if you performed extensive Google searches) to provide:
        *   **Links between News:** Explicitly connect disparate news items to show larger trends.
        *   **Context:** Explain the 'why' and 'how' behind events, drawing on industry knowledge.
        *   **Perspective:** Offer different viewpoints or implications for miners.
        *   **Insights:** Provide forward-looking analysis or strategic takeaways for the readership.
        *   This grounding must primarily focus on:
            *   **Energy Market:** (e.g., costs, sources, demand, competition from AI/HPC, grid stability)
            *   **Politics/Regulation:** (e.g., government incentives, legislative debates, local impacts, international policies affecting mining)
            *   **ASIC Manufacturing/Hardware:** (e.g., market trends, repurposing challenges, financing implications for new hardware, supply chain)
    3.  **Bitcoin-Only Focus:** The content must refer ONLY to Bitcoin. Do NOT use the word "crypto" or refer to any other cryptocurrency.
    4.  **Relevance to Miners:** All insights and context must be highly relevant and actionable for Bitcoin miners, directly addressing their interests, challenges, and opportunities.
    5.  **Identify Trends:** Clearly highlight overarching industry trends (e.g., the pivot to AI, evolving energy strategies, hardware investment shifts).

    **Formatting & Style Constraints:**
    *   **Output Format:** Provide the full brief in **Markdown format**.
    *   **No Em Dashes:** Do not use em dashes (—). Use commas, periods, or other standard punctuation as needed.
    *   **Clickable Hyperlinks:** All references to source URLs MUST be embedded directly as clickable hyperlinks within the text. Do NOT use parenthetical citations or a separate "Sources" section.
    *   **Clear Headings:** Use clear, concise, and bolded headings for different sections (e.g., "**Operational Shifts**," "**Energy & Policy Watch**").
    *   **Bulleted Lists:** Use standard bullet points (`*`) for key takeaways or summarized points within sections.
    *   **Production Ready:** The output must be completely production-ready, without any notes, administrative messages, or meta-commentary from you.

    **Input Articles and Context:**
    {full_context_for_gemini}

    **Begin the Daily Brief below, starting with the exact theme line:**
    """
    brief_content_md = _robust_generate_content(prompt)

    if brief_content_md and brief_content_md.startswith("Today, in Bitcoin Mining:"):
        brief_title = brief_content_md.split('\n')[0].strip() # Get the first line as the title
        brief_deck = generate_brief_deck(brief_content_md) # Generate deck from full content
        brief_themes = identify_daily_themes_with_gemini(brief_content_md) # Identify themes

        return {
            "brief_title": brief_title,
            "brief_deck": brief_deck,
            "brief_content_md": brief_content_md,
            "brief_themes": brief_themes
        }
    else:
        logging.error("Failed to generate main brief content or it did not start with the expected theme.")
        return {"brief_title": "ERROR: Brief generation failed", "brief_deck": "Could not generate brief content.", "brief_content_md": "Error.", "brief_themes": []}


# Legacy/Compatibility functions for backward compatibility with existing code
def generate_daily_brief_markdown(articles: List[Dict], date) -> str:
    """
    Generates a Markdown formatted daily brief from collected articles.
    This is a compatibility wrapper for the existing daily_brief_script.py.
    
    Args:
        articles: List of article dicts with keys: title, url, summary, source
        date: Date for the brief (datetime object)
    
    Returns:
        Markdown formatted string
    """
    from datetime import datetime
    date_str = date.strftime("%Y-%m-%d")
    formatted_date = date.strftime("%B %d, %Y")
    
    md_content = f"""# Bitcoin Mining Daily Brief - {formatted_date}

## Executive Summary

This brief summarizes {len(articles)} key developments in the Bitcoin mining industry for {formatted_date}.

---

## Top Stories

"""
    
    for idx, article in enumerate(articles, 1):
        title = article.get('title', 'Untitled')
        url = article.get('url', '#')
        summary = article.get('summary', 'No summary available.')
        source = article.get('source', 'Unknown Source')
        
        md_content += f"""### {idx}. {title}

**Source:** {source}

{summary}

[Read Full Article]({url})

---

"""
    
    md_content += f"""
## About This Brief

This brief is automatically generated by the SHA256 News Bitcoin Mining Aggregator Bot. It compiles and summarizes relevant news articles from across the web, focusing exclusively on Bitcoin mining operations, market developments, and related infrastructure.

**Date:** {formatted_date}  
**Articles Covered:** {len(articles)}

---

*For more updates, follow us on Twitter [@SHA256News](https://twitter.com/SHA256News)*
"""
    
    return md_content


def convert_markdown_to_html(md_content: str, brief_date) -> str:
    """
    Converts Markdown content to HTML using a template.
    
    Args:
        md_content: Markdown formatted content
        brief_date: Date of the brief (datetime object)
    
    Returns:
        Full HTML page as string
    """
    from datetime import datetime
    # Convert markdown to HTML
    html_body = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
    
    date_str = brief_date.strftime("%Y-%m-%d")
    formatted_date = brief_date.strftime("%B %d, %Y")
    
    # Create full HTML page
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Bitcoin Mining Daily Brief for {formatted_date}">
    <title>Bitcoin Mining Daily Brief - {formatted_date} | SHA256 News</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        h1 {{
            color: #f7931a;
            border-bottom: 3px solid #f7931a;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #333;
            margin-top: 30px;
        }}
        h3 {{
            color: #555;
        }}
        a {{
            color: #f7931a;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 20px 0;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .meta {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
"""
    
    return html_template


def generate_brief_metadata(md_content: str, brief_date) -> Dict:
    """
    Generates metadata for a brief including deck and themes.
    
    Args:
        md_content: Markdown content of the brief
        brief_date: Date of the brief (datetime object)
    
    Returns:
        Dict with metadata
    """
    from datetime import datetime
    deck = generate_brief_deck(md_content)
    themes = identify_daily_themes_with_gemini(md_content)
    
    return {
        'date': brief_date.strftime("%Y-%m-%d"),
        'formatted_date': brief_date.strftime("%B %d, %Y"),
        'deck': deck,
        'themes': themes,
        'url': f"/briefs/brief-{brief_date.strftime('%Y-%m-%d')}.html"
    }
