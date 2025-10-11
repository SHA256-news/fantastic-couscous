# Model Context Protocol (MCP) - Bitcoin Mining News Bot

This document provides comprehensive context for AI assistants working with this codebase.

## Project Overview

**Name**: Bitcoin Mining News Aggregator Bot (SHA256.news)  
**Type**: Automated news aggregation and publishing system  
**Language**: Python 3.11+  
**Architecture**: Modular, event-driven with GitHub Actions automation  
**Purpose**: Aggregate, analyze, and disseminate Bitcoin mining news via Twitter and web

## Core Components

### 1. News Processing (`news_processor.py`)
- **Responsibility**: Fetch and extract Bitcoin mining news
- **Data Sources**: Event Registry API, RSS feeds, web scraping
- **Key Features**:
  - Mining-specific keyword filtering
  - Content extraction from URLs
  - Duplicate detection
  - Article metadata collection

### 2. AI Interface (`gemini_interface.py`)
- **Responsibility**: AI-powered content analysis and generation
- **Model**: Google Gemini Pro
- **Capabilities**:
  - Article summarization and enhancement
  - Tweet content generation
  - Trend identification
  - Search query optimization
  - Daily brief generation

### 3. Twitter Publisher (`twitter_publisher.py`)
- **Responsibility**: Twitter API integration
- **API Version**: Twitter API v2 with OAuth 1.0a
- **Features**:
  - Single tweet publishing with media
  - Thread creation
  - Rate limit handling
  - Error recovery

### 4. Image Manager (`image_manager.py`)
- **Responsibility**: Intelligent image selection
- **Strategy**:
  1. Company logo matching (e.g., Bitmain, MicroBT)
  2. Topic-based conceptual images
  3. Default Bitcoin logo fallback
- **Image Types**: PNG, JPG/JPEG

### 5. Daily Brief Generator (`daily_brief_generator.py`)
- **Responsibility**: Create comprehensive daily summaries
- **Process**:
  1. Aggregate 24-hour articles
  2. Identify trends with Gemini
  3. Generate structured content
  4. Produce HTML output
  5. Update website index

### 6. GitHub Manager (`github_manager.py`)
- **Responsibility**: State persistence and GitHub integration
- **Features**:
  - Bot state storage (`bot_state.json`)
  - GitHub Pages content updates
  - JSON feed generation
  - File operations via PyGithub

## Data Flow

### Tweet Publishing Flow
```
Event Registry → News Processor → Article Queue (LIFO)
                                      ↓
                            Gemini Enhancement
                                      ↓
                            Image Selection
                                      ↓
                            Tweet Generation
                                      ↓
                          Twitter Publication
                                      ↓
                      State Update + Website Update
```

### Daily Brief Flow
```
Last 24h Articles → Trend Analysis (Gemini)
                          ↓
              Brief Content Generation (Gemini)
                          ↓
                  HTML Formatting
                          ↓
              File Write + Index Update
                          ↓
              GitHub Pages Deployment
```

## State Management

### Bot State Structure
```json
{
  "version": "1.0",
  "initialized_at": "ISO-8601",
  "last_run": "ISO-8601",
  "article_queue": [
    {
      "title": "string",
      "url": "string",
      "source": "string",
      "published_date": "ISO-8601",
      "body": "string",
      "image": "string",
      "ai_summary": "string",
      "ai_topics": ["string"],
      "ai_sentiment": "positive|neutral|negative",
      "ai_significance": 1-10
    }
  ],
  "published_articles": [
    {
      "title": "string",
      "url": "string",
      "published_at": "ISO-8601",
      "tweet_id": "string"
    }
  ],
  "daily_briefs": [
    {
      "date": "YYYY-MM-DD",
      "filename": "string",
      "url": "string",
      "headline": "string"
    }
  ]
}
```

### Queue Management
- **Type**: LIFO (Last In, First Out)
- **Operation**: New articles inserted at position 0
- **Processing**: Articles taken from position 0
- **Deduplication**: URL-based before insertion
- **Failure Handling**: Failed articles re-inserted at position 0

## Automation

### GitHub Actions Workflows

#### Main Workflow (`main.yml`)
- **Schedule**: Every 4 hours
- **Trigger**: Cron + Manual
- **Steps**:
  1. Checkout repository
  2. Setup Python 3.11
  3. Install dependencies
  4. Run bot (`main.py`)
  5. Commit state changes
  6. Upload logs

#### Brief Workflow (`publish_brief.yml`)
- **Schedule**: Daily at 8 AM UTC
- **Trigger**: Cron + Manual
- **Steps**:
  1. Checkout repository
  2. Setup Python 3.11
  3. Generate brief (inline Python)
  4. Commit brief files
  5. Deploy to GitHub Pages

## Configuration

### Environment Variables
- **Required**:
  - `TWITTER_API_KEY`, `TWITTER_API_SECRET`
  - `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`
  - `TWITTER_BEARER_TOKEN`
  - `GEMINI_API_KEY`
  - `EVENT_REGISTRY_API_KEY`
  
- **Optional**:
  - `GITHUB_TOKEN` (for state sync)
  - `GITHUB_REPO` (format: owner/repo)
  - `LOG_LEVEL` (default: INFO)
  - `BOT_STATE_FILE` (default: bot_state.json)

### Directory Structure
```
bitcoin_miner_bot/
├── *.py              # Python modules
├── bot_state.json    # Persistent state
├── bot.log          # Log file
├── .env             # Local config (not committed)
├── .env.example     # Config template
├── .github/workflows/  # Automation
├── images/          # Image assets
│   ├── company_logos/
│   └── conceptual/
└── gh-pages/        # Website content
    ├── index.html
    ├── *.json       # Data feeds
    └── briefs/      # Brief archive
```

## API Integration

### Event Registry
- **Purpose**: Primary news source
- **Endpoint**: QueryArticlesIter
- **Filters**: Bitcoin mining keywords, English, last 24h
- **Rate Limits**: Based on API tier

### Google Gemini
- **Model**: gemini-pro
- **Use Cases**: 
  - Article analysis (max ~2000 chars input)
  - Tweet generation (240 chars output)
  - Trend identification
  - Brief content generation
- **Response Format**: JSON when requested
- **Error Handling**: Fallback to simple text processing

### Twitter API v2
- **Authentication**: OAuth 1.0a + Bearer Token
- **Media Upload**: v1.1 API endpoint
- **Rate Limits**:
  - Tweets: 300 per 3 hours
  - Media: 300 per 3 hours
- **Features Used**: create_tweet, media_upload

### GitHub API (PyGithub)
- **Purpose**: State sync, file operations
- **Methods**: get_repo, get_contents, update_file, create_file
- **Branch**: main (for state), gh-pages (for website)

## Error Handling

### Logging Strategy
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Targets**: File (`bot.log`) + Console
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

### Recovery Mechanisms
1. **API Failures**: Log and continue, use fallback methods
2. **Queue Errors**: Re-insert articles for retry
3. **State Corruption**: Revert to default state structure
4. **Network Issues**: Retry with exponential backoff (implicit in libs)

## Extensibility

### Adding News Sources
1. Implement fetcher in `news_processor.py`
2. Add to `fetch_articles()` method
3. Ensure consistent article dictionary format

### Adding Image Categories
1. Add images to appropriate directory
2. Update mappings in `image_manager.py`:
   - `company_mappings` for logos
   - `topic_images` for concepts

### Modifying Tweet Format
- Edit `gemini_interface.py::generate_tweet_content()`
- Adjust prompt and constraints
- Test character limits (280 total, ~240 for text)

### Customizing Briefs
- Modify `daily_brief_generator.py::_generate_html()`
- Update `brief_template.html` template
- Adjust Gemini prompts for different content structure

## Best Practices

### When Modifying Code
1. Maintain logging at appropriate levels
2. Update docstrings for public methods
3. Handle exceptions gracefully
4. Preserve backwards compatibility of state structure
5. Test with mock data before live APIs

### When Debugging
1. Check `bot.log` for detailed trace
2. Verify environment variables are set
3. Test individual modules in isolation
4. Use `workflow_dispatch` for manual test runs
5. Review GitHub Actions logs

### When Adding Features
1. Follow existing module patterns
2. Add configuration via environment variables
3. Document in README.md
4. Update this MCP document
5. Consider impact on state structure

## Common Patterns

### Article Dictionary Format
```python
{
    'title': str,
    'url': str,
    'source': str,
    'published_date': str (ISO-8601),
    'body': str,
    'image': str (URL),
    'fetched_at': str (ISO-8601),
    'ai_summary': str (optional),
    'ai_topics': list[str] (optional),
    'ai_sentiment': str (optional),
    'ai_significance': int (optional),
    'extracted_content': bool (optional)
}
```

### Logging Pattern
```python
logger = logging.getLogger(__name__)
logger.info("Informational message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
```

### Error Handling Pattern
```python
try:
    # operation
    logger.info("Success message")
except SpecificException as e:
    logger.error(f"Error: {e}", exc_info=True)
    # fallback or recovery
```

## Security Considerations

1. **Secrets Management**: All API keys via environment variables
2. **No Commits**: `.env` in `.gitignore`
3. **GitHub Secrets**: Use repository secrets for Actions
4. **Token Permissions**: Minimal required scopes
5. **Input Validation**: Sanitize URLs and user-generated content

## Performance Considerations

1. **Batch Processing**: Up to 5 articles per run (configurable)
2. **Rate Limiting**: Respect API limits (300 tweets/3h)
3. **Content Limits**: Trim article bodies to 5000 chars
4. **Image Caching**: Local file system for images
5. **State Size**: Keep last 100 published articles only

## Testing Approach

### Manual Testing
```bash
# Test individual modules
python -c "from news_processor import NewsProcessor; print(NewsProcessor().fetch_articles(1))"

# Test with mock data
# Create test article dictionary and pass to functions
```

### Integration Testing
- Use `workflow_dispatch` in GitHub Actions
- Monitor logs in Actions tab
- Verify outputs on Twitter and website

## Future Enhancements

Potential areas for expansion:
1. Additional news sources (RSS parsers, APIs)
2. More sophisticated trend analysis
3. Thread generation for long-form content
4. Image generation via AI
5. User interaction handling (replies, mentions)
6. Multi-platform publishing (LinkedIn, Mastodon)
7. Email newsletter generation
8. Real-time monitoring dashboard

## Support Resources

- **Python Docs**: https://docs.python.org/3/
- **Tweepy Docs**: https://docs.tweepy.org/
- **Gemini Docs**: https://ai.google.dev/docs
- **PyGithub Docs**: https://pygithub.readthedocs.io/
- **Event Registry Docs**: https://eventregistry.org/documentation
- **GitHub Actions Docs**: https://docs.github.com/actions

## Maintenance

### Regular Tasks
- Monitor API quotas and usage
- Review and clean bot logs
- Update dependencies (monthly)
- Audit published content quality
- Refresh image assets
- Backup state file

### Monitoring Metrics
- Articles fetched per run
- Tweets published per day
- API error rates
- Queue depth
- Processing latency
- Brief generation success rate

---

*This MCP is a living document. Update it as the system evolves.*
