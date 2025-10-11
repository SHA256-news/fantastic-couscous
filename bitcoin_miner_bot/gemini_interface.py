# gemini_interface.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Ensure the correct Gemini model is used
GEMINI_MODEL = 'gemini-pro' # Use 'gemini-1.5-pro-latest' for newer models if available and configured.

def semantically_filter_article(article_title: str, article_summary: str, article_text: str) -> bool:
    """
    Uses Gemini to semantically filter articles for Bitcoin-only mining relevance.
    Returns True if the article is primarily about Bitcoin mining, False otherwise.
    """
    # Truncate article_text to fit within typical model context limits (e.g., ~15,000 characters)
    combined_text = f"Title: {article_title}\nSummary: {article_summary}\nBody: {article_text[:15000]}" # 15k chars is a rough safety limit

    prompt = f"""
    Analyze the following article text to determine if its *primary and overarching focus* is exclusively on Bitcoin mining operations, market, or related infrastructure.

    **Criteria for "Relevant":**
    - The article must be about Bitcoin.
    - The article must specifically discuss Bitcoin *mining*, miners, mining hardware (ASICs), mining profitability, mining infrastructure (data centers), or companies primarily involved in Bitcoin mining (e.g., Riot Platforms, Marathon Digital, CleanSpark, Bitfarms, Iris Energy, Hive Digital).
    - Incidental mentions of other cryptocurrencies (e.g., "Ethereum," "Solana," "DeFi," "NFTs") that are not the main subject should generally be ignored, UNLESS the article is discussing a company's pivot from Bitcoin mining to other areas (e.g., AI/HPC for former mining sites) where Bitcoin mining's historical context is central.

    **Detailed Explanation of "Relevant" Criteria (for nuanced filtering):**
    This rule instructs you to:
    1.  Be **forgiving** of minor, non-focal mentions of other cryptocurrencies or related technologies when the core topic is clearly Bitcoin mining. If another cryptocurrency is mentioned briefly for comparison or as a passing reference, and the main thrust of the article is still Bitcoin mining, the article IS relevant.
    2.  Be **intelligent** enough to recognize that articles about a *pivot away from Bitcoin mining* (e.g., towards AI, HPC, or other digital asset ventures) are still highly relevant *to the Bitcoin mining community* if the discussion explicitly links back to:
        *   The company's Bitcoin mining history.
        *   Repurposing of assets originally built for Bitcoin mining.
        *   The reasons for the transition (e.g., waning Bitcoin mining profitability).
        *   The strategic implications for the Bitcoin mining industry.
    In such pivot scenarios, even if the new focus isn't Bitcoin mining, the article's context makes it highly pertinent for your target audience.

    **Criteria for "Not Relevant":**
    - The primary focus is on cryptocurrencies *other than* Bitcoin.
    - The primary focus is on general blockchain technology, NFTs, DeFi, smart contracts, or specific altcoins.
    - The mention of Bitcoin mining is extremely superficial or a very minor part of an otherwise unrelated article.

    Return only one of the following exact strings:
    "RELEVANT_BITCOIN_MINING"
    "NOT_RELEVANT"

    Article Text:
    ---
    {combined_text}
    ---
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        if response and response.candidates and response.candidates[0].content.parts:
            result = response.candidates[0].content.parts[0].text.strip()
            return result == "RELEVANT_BITCOIN_MINING"
        return False
    except Exception as e:
        print(f"DEBUG: Error filtering article with Gemini: {e}")
        # Log more details if needed, e.g., article ID
        return False # Default to not relevant on error


def generate_tweet_content(article_title: str, article_content: str, article_url_title: str) -> str:
    """
    Generates a catchy headline and 3-point summary for a tweet using Gemini.
    Adheres to all specific formatting and content constraints.
    """
    # Truncate article_content to fit within typical model context limits
    truncated_content = article_content[:30000] # Use a generous limit, adjust if needed

    prompt = f"""
    You are a Twitter news aggregator bot for Bitcoin mining articles. Your task is to create a catchy headline and a 3-point summary for a given article.

    **Article URL Title:** {article_url_title}
    **Article Content:**
    {truncated_content}

    **Instructions:**
    1.  Generate a single, catchy headline that is highly engaging and optimized for Twitter. It should contain no punctuation, unless it is a question mark at the end of a question.
    2.  Generate a 3-point summary that highlights the most critical, recent, and specific information from the article. Each point must be a bullet point. Each bullet point should contain no punctuation, unless it is a question mark at the end of a question.
    3.  **Specifics Allowed for Repetition:** Specific facts about "who, what, how much, where, when" from the 'Article URL Title' can be repeated in the headline or summary. However, the *angle* or *implied significance* of the headline/summary should still offer something fresh.
    4.  **Crucially, the headline and each point of the summary must not repeat general information explicitly stated in the 'Article URL Title' provided above.** They must offer new, relevant, and specific details, beyond the allowed specific facts.
    5.  **Bitcoin-Only Focus:** The content must refer ONLY to Bitcoin. Do NOT use the word "crypto" or refer to any other cryptocurrency. Ensure it is highly relevant to what Bitcoin miners are interested in reading.
    6.  **Ethical Journalism:** Adhere strictly to the tenets of ethical journalism: truth, accuracy, independence, fairness, impartiality, humanity, and accountability. The content should be factual, unbiased, and provide context.
    7.  The combined length of the headline and the 3-point summary (including line breaks) must not exceed 280 characters.
    8.  Ensure the summary points are clear, concise, and provide distinct insights. Do not truncate any part of the headline or summary points.

    **Format your output as follows:**
    [Catchy Headline (no punctuation unless question mark)]
    • [Summary Point 1 (no punctuation unless question mark)]
    • [Summary Point 2 (no punctuation unless question mark)]
    • [Summary Point 3 (no punctuation unless question mark)]
    """
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        if response and response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text.strip()
        return "Could not generate tweet content."
    except Exception as e:
        print(f"DEBUG: Error generating tweet content with Gemini: {e}")
        return f"Error generating tweet content: {e}"
