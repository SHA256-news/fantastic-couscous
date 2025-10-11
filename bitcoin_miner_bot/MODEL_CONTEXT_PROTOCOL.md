# Model Context Protocol

## Overview
This document describes the protocol and guidelines for AI model interactions within the Bitcoin Mining News Aggregator Bot.

## Models Used

### Google Gemini Pro
- **Primary Model**: `gemini-pro`
- **Fallback**: `gemini-1.5-pro-latest` (if configured)
- **Purpose**: Content filtering, tweet generation, and daily brief creation

## Use Cases

### 1. Article Filtering (`semantically_filter_article`)
**Purpose**: Determine if an article is primarily about Bitcoin mining

**Input**:
- Article title
- Article summary
- Article body text (truncated to 15,000 characters)

**Output**:
- Boolean: True if relevant, False if not relevant
- Based on exact string match: "RELEVANT_BITCOIN_MINING"

**Filtering Criteria**:
- Must be about Bitcoin (not other cryptocurrencies)
- Must focus on mining operations, miners, hardware, or related infrastructure
- Must involve Bitcoin mining companies or market dynamics
- Should be intelligent about pivots (e.g., mining companies moving to AI/HPC)

### 2. Tweet Generation (`generate_tweet_content`)
**Purpose**: Create engaging, concise tweet content from articles

**Input**:
- Article title
- Article content (truncated to 30,000 characters)
- Article URL title for context

**Output**:
- Formatted string with headline and 3-point summary
- Format: `[Headline]\n• [Point 1]\n• [Point 2]\n• [Point 3]`

**Content Requirements**:
- Total length ≤ 280 characters (including line breaks)
- No punctuation except question marks at end of questions
- Bitcoin-only focus (no "crypto" or other cryptocurrencies)
- Ethical journalism principles
- Specific, actionable information
- No repetition of general info from URL title

### 3. Daily Brief Generation (`generate_daily_brief`)
**Purpose**: Create comprehensive daily summaries of Bitcoin mining news

**Input**:
- List of articles (up to 20,000 characters of combined text)
- Date string

**Output**:
- Markdown-formatted comprehensive brief
- Organized by themes (operations, market, technology, regulatory)
- Executive summary and "Looking Ahead" sections

**Content Requirements**:
- Professional, objective tone
- Specific data points and company names
- Bitcoin-only focus
- Clear markdown formatting with headers and bullets
- Source attribution with inline links

## Error Handling

### API Failures
- All functions have try-catch blocks
- Errors are logged with DEBUG prefix
- Default return values on error:
  - `semantically_filter_article`: False (not relevant)
  - `generate_tweet_content`: Error message string
  - `generate_daily_brief`: Error notice in markdown

### Rate Limiting
- No built-in rate limiting (relies on API SDK)
- Consider implementing exponential backoff for production

## Context Window Management

### Token Limits
- `semantically_filter_article`: 15,000 chars
- `generate_tweet_content`: 30,000 chars
- `generate_daily_brief`: 20,000 chars

### Truncation Strategy
- Simple character-based truncation
- May cut mid-sentence
- Consider implementing smart truncation at sentence boundaries for production

## Best Practices

1. **Always validate API key** is set before making calls
2. **Log all interactions** for debugging and auditing
3. **Handle partial responses** gracefully
4. **Monitor API costs** in production
5. **Test with sample data** before deploying
6. **Implement retries** for transient failures
7. **Cache results** where appropriate to reduce API calls

## Future Enhancements

1. Implement fine-tuned models for Bitcoin mining domain
2. Add response caching layer
3. Implement streaming responses for long content
4. Add A/B testing for different prompts
5. Implement prompt versioning and rollback
6. Add model performance metrics and monitoring
