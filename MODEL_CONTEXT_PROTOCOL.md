# Model Context Protocol (MCP) - SHA256 News Bot

This document defines the context and protocols for AI models working with the SHA256 News Bitcoin Mining News Aggregator Bot.

## Project Overview

SHA256 News is an automated news aggregation bot that focuses exclusively on Bitcoin mining. It uses AI to filter articles, generate tweet content, and create daily briefs.

## Core Principles

### 1. Bitcoin-Only Focus
- All content must be exclusively about Bitcoin
- No mentions of "crypto" or other cryptocurrencies unless contextually necessary
- Focus on mining operations, hardware, companies, and infrastructure

### 2. Ethical Journalism Standards
- Truth and accuracy above all
- Independence and fairness
- Unbiased reporting
- Provide context and accountability

### 3. Quality Over Quantity
- Better to skip an article than publish irrelevant content
- Prioritize recent, specific, and actionable information
- Avoid generic or superficial content

## Module Contexts

### gemini_interface.py

**Purpose**: AI-powered content analysis and generation

**Key Functions**:
- `semantically_filter_article()`: Determines Bitcoin mining relevance
- `generate_tweet_content()`: Creates engaging headlines and summaries
- `generate_brief_deck()`: Summarizes daily briefs
- `generate_thematic_trends()`: Identifies overarching themes

**Model Behavior**:
- Be strict about Bitcoin-only criteria
- Be forgiving of minor altcoin mentions if Bitcoin mining is the focus
- Recognize pivot stories (e.g., mining companies moving to AI) as relevant
- Generate concise, engaging content within character limits
- Avoid punctuation except question marks
- Never repeat general information from URL title

### news_processor.py

**Purpose**: Article fetching and content extraction

**Key Functions**:
- `fetch_article_content()`: Extracts clean article text
- `get_articles_from_eventregistry()`: Queries EventRegistry API

**Processing Logic**:
- Use ordered CSS selectors for robust extraction
- Filter out boilerplate and short paragraphs
- Handle errors gracefully
- Deduplicate by URL and event URI

### twitter_publisher.py

**Purpose**: Tweet publication with media

**Key Functions**:
- `publish_tweet()`: Publishes tweet with optional images
- `upload_and_attach_images()`: Handles media uploads

**Publishing Protocol**:
- Main tweet contains generated content + image
- Reply tweet contains source URL
- Track tweet metadata for website integration

### image_manager.py

**Purpose**: Image selection and management

**Selection Logic**:
1. Check if IMAGE_LIBRARY_ACTIVE is enabled
2. Match company names to logos
3. Fallback to random conceptual image
4. Return None if no images available

### daily_brief_generator.py

**Purpose**: Daily brief compilation

**Format**:
- Markdown source
- HTML output with styling
- Metadata for website integration

## State Management Protocol

### bot_state.json Structure
```json
{
  "processed_urls": ["url1", "url2"],
  "processed_event_uris": ["uri1", "uri2"],
  "daily_brief_urls": ["url3", "url4"],
  "lifo_queue": [
    {
      "url": "...",
      "event_uri": "...",
      "html_title": "...",
      "article_url_title": "...",
      "full_content": "...",
      "er_title": "...",
      "er_summary": "...",
      "source_title": "..."
    }
  ],
  "last_run": "2025-01-01T12:00:00",
  "last_brief_date": "2025-01-01T18:00:00"
}
```

### State Persistence Rules
1. Load state at bot initialization
2. Restore globals in news_processor
3. Save state after each successful tweet
4. Push state to GitHub for persistence
5. Clear daily_brief_urls after brief publication

## API Integration Protocols

### Google Gemini
- Model: Configurable via GEMINI_MODEL env var
- Default: "gemini-pro"
- Handle response structure variations robustly
- Truncate inputs to stay within context limits

### EventRegistry
- Query by Bitcoin mining concept URI
- 4-hour lookback window
- Sort by date, most recent first
- Max 100 articles per query

### Twitter (Tweepy)
- Use v2 API (Client) for tweets
- Use v1.1 API for media uploads
- Handle rate limits gracefully
- Construct permalinks from username + tweet ID

### GitHub (PyGithub)
- Use PAT with repo scope
- Update/create files in gh-pages
- Handle existing file updates
- Create files if they don't exist

## Content Generation Guidelines

### Tweet Headlines
- Engaging and optimized for Twitter
- No punctuation except question marks
- Don't repeat URL title general info
- Can repeat specific facts (who, what, when, where, how much)
- Maximum 280 characters total (headline + summary)

### Tweet Summaries
- 3 bullet points
- Distinct, specific insights
- No punctuation except question marks
- Provide context and significance
- Focus on what miners care about

### Daily Brief Format
```markdown
# Bitcoin Mining Daily Brief - [Date]

## Executive Summary
[Summary of articles count and date]

---

## Top Stories

### 1. [Article Title]
**Source:** [Source Name]
[Summary]
[Read Full Article](url)

---

[Repeat for each article]

## About This Brief
[Boilerplate information]
```

## Error Handling Protocols

### Network Errors
- Log warning, don't crash
- Return empty/error state
- Allow bot to continue with next article

### API Errors
- Log error with context
- Handle rate limits
- Use fallbacks where appropriate

### Content Errors
- Skip articles with insufficient content
- Use generic fallbacks for failed generations
- Never publish error messages to Twitter

## Testing Guidelines

### Local Testing
- Use .env file for credentials
- Test individual modules
- Verify state persistence
- Check log output

### Production Testing
- Use GitHub Secrets
- Monitor GitHub Actions logs
- Review bot.log artifacts
- Verify website updates

## Maintenance Protocols

### Regular Tasks
- Monitor API usage and costs
- Review filtering accuracy
- Update company logo mappings
- Refresh conceptual images
- Archive old briefs

### Emergency Procedures
- Disable workflows if needed
- Review and roll back state
- Rotate compromised credentials
- Clear queue if malformed

## Extension Points

### Future Enhancements
- Custom search API for grounding
- Email alerts for breaking news
- Expanded image library
- Multi-language support
- Advanced analytics dashboard

### Integration Placeholders
- GOOGLE_CUSTOM_SEARCH_API_KEY
- GOOGLE_CUSTOM_SEARCH_CX
- ALERT_EMAIL_RECIPIENT
- SENDGRID_API_KEY

## Version History

- v1.0.0 (2025): Initial implementation with full AI-powered pipeline

---

This protocol ensures consistent behavior across all AI interactions with the SHA256 News bot codebase.