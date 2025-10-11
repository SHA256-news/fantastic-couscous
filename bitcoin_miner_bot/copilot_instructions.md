# GitHub Copilot Instructions for Bitcoin Mining News Bot

## Project Context

This is an automated Bitcoin mining news aggregator bot that:
- Fetches news from Event Registry API
- Enhances content with Google Gemini AI
- Publishes to Twitter with intelligent image selection
- Generates daily briefs
- Maintains a GitHub Pages website

## Code Style Guidelines

### Python Style
- Follow PEP 8 conventions
- Use descriptive variable names
- Add docstrings to all public functions and classes
- Type hints encouraged but not required
- Maximum line length: 100 characters

### Naming Conventions
- Classes: `PascalCase` (e.g., `NewsProcessor`)
- Functions/Methods: `snake_case` (e.g., `fetch_articles`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `LOG_LEVEL`)
- Private methods: `_leading_underscore` (e.g., `_extract_content`)

### Logging
Always use the logging module:
```python
import logging
logger = logging.getLogger(__name__)

# Usage
logger.info("Informational message")
logger.warning("Warning about potential issue")
logger.error("Error occurred", exc_info=True)
logger.debug("Detailed debugging info")
```

### Error Handling
Wrap operations in try-except blocks:
```python
try:
    # risky operation
    logger.info("Operation succeeded")
except SpecificException as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    # graceful fallback
```

## Module-Specific Guidelines

### news_processor.py
- Always validate URLs before fetching
- Limit article body to 5000 characters
- Use BeautifulSoup with 'lxml' parser
- Filter for mining-relevant content
- Handle network timeouts gracefully

### gemini_interface.py
- Request JSON responses when possible
- Limit input text to ~2000 characters
- Provide fallback for missing API key
- Handle JSON parsing errors
- Keep prompts clear and specific

### twitter_publisher.py
- Respect 280 character limit (240 for text + URL)
- Always check if client is initialized
- Handle rate limit errors gracefully
- Use v1.1 API for media upload
- Return structured result dictionaries

### image_manager.py
- Check file existence before returning paths
- Provide sensible fallbacks
- Log image selection decisions at INFO level
- Support PNG, JPG, JPEG formats
- Case-insensitive matching for company names

### daily_brief_generator.py
- Generate valid HTML
- Include proper meta tags
- Make briefs mobile-responsive
- Link back to main website
- Update index after each brief

### github_manager.py
- Always check if GitHub is configured
- Handle file not found gracefully
- Update timestamps on state changes
- Keep published articles list bounded (100 max)
- Log all GitHub operations

## Common Patterns

### Configuration Loading
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

if not api_key:
    logger.warning("API_KEY not configured")
    # provide fallback behavior
```

### Article Dictionary Structure
```python
article = {
    'title': str,
    'url': str,
    'source': str,
    'published_date': str,  # ISO-8601
    'body': str,
    'image': str,           # URL
    'fetched_at': str,      # ISO-8601
    # Optional AI fields
    'ai_summary': str,
    'ai_topics': list[str],
    'ai_sentiment': str,
    'ai_significance': int
}
```

### State Management
```python
# Load state
state = github_manager.load_state()

# Modify state
state['last_run'] = datetime.now().isoformat()
state['article_queue'].insert(0, article)  # LIFO

# Save state
github_manager.save_state(state)
```

## API Integration Notes

### Event Registry
- Use `QueryArticlesIter` for time-range queries
- Filter by language: `lang="eng"`
- Use OR for multiple keywords
- Handle pagination automatically

### Google Gemini
- Model: `gemini-pro`
- Request structured JSON when possible
- Handle rate limits and quotas
- Provide context in prompts
- Parse responses defensively

### Twitter API v2
- Use OAuth 1.0a for authentication
- Bearer token for read operations
- v1.1 API for media upload
- Check response.data for tweet ID
- Handle TweepyException specifically

## Testing Suggestions

### Unit Testing
```python
# Test individual functions with mock data
def test_article_processing():
    mock_article = {
        'title': 'Test Article',
        'url': 'https://example.com',
        'body': 'Test content'
    }
    # test function
```

### Integration Testing
```python
# Test full workflow with real APIs (use sparingly)
# Set up .env with test credentials
# Run main.py with limited articles
```

### Manual Testing
```bash
# Test news fetching
python -c "from news_processor import NewsProcessor; n = NewsProcessor(); print(len(n.fetch_articles(5)))"

# Test Gemini
python -c "from gemini_interface import GeminiInterface; g = GeminiInterface(); print(g.generate_tweet_content({'title': 'Test', 'body': 'Test'}))"
```

## Common Issues and Solutions

### Issue: No articles fetched
**Check:**
- Event Registry API key validity
- Network connectivity
- API quota not exceeded
**Solution:** Add fallback to RSS parsing or mock data

### Issue: Twitter publishing fails
**Check:**
- API credentials correct and active
- Rate limits not exceeded (300/3h)
- Tweet length under 280 chars
**Solution:** Implement retry logic with exponential backoff

### Issue: Gemini errors
**Check:**
- API key valid
- Input text length (<2000 chars)
- Request quota not exceeded
**Solution:** Provide simple fallback without AI

### Issue: State not persisting
**Check:**
- bot_state.json file permissions
- GitHub token has write access
- Repository name format (owner/repo)
**Solution:** Verify local file write first, then GitHub sync

## Security Best Practices

1. **Never commit secrets**: Use .env (in .gitignore)
2. **Validate inputs**: Sanitize URLs, user content
3. **Limit permissions**: Use minimal token scopes
4. **Rate limiting**: Respect API limits
5. **Error messages**: Don't expose secrets in logs

## Performance Optimization

1. **Batch operations**: Process 5 articles per run
2. **Limit content**: Trim bodies to reasonable size
3. **Cache when possible**: Store processed data
4. **Async where beneficial**: Consider for network ops
5. **Monitor resources**: Log processing times

## Documentation Requirements

### Function Docstrings
```python
def process_article(article, enhance=True):
    """
    Process and enhance a news article.
    
    Args:
        article: Article dictionary with title, url, body
        enhance: Whether to enhance with AI (default: True)
        
    Returns:
        Enhanced article dictionary
        
    Raises:
        ValueError: If article is missing required fields
    """
```

### Module Docstrings
```python
"""
Module Name

Brief description of module purpose and functionality.
Key features and responsibilities.
"""
```

## Git Commit Messages

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
- `feat: add company logo detection`
- `fix: handle Twitter rate limiting`
- `docs: update README with setup instructions`

## When Adding New Features

1. **Plan**: Document the feature in comments first
2. **Implement**: Write code following existing patterns
3. **Log**: Add appropriate logging statements
4. **Error Handle**: Wrap in try-except blocks
5. **Test**: Verify with sample data
6. **Document**: Update README and this file
7. **Review**: Check for security and performance issues

## Quick Reference

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

### File Operations
```python
# Always use context managers
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
```

### JSON Handling
```python
# Reading
with open(file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Writing
with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

### Datetime Format
```python
from datetime import datetime

# ISO-8601 format for consistency
now = datetime.now().isoformat()
date_str = datetime.now().strftime('%Y-%m-%d')
```

## Questions to Consider

When modifying code, ask:
1. Does this maintain backwards compatibility?
2. Are errors handled gracefully?
3. Is logging at the appropriate level?
4. Will this work without API keys (fallback)?
5. Is the impact on state structure considered?
6. Are rate limits respected?
7. Is the code self-documenting?

## Resources

- [PEP 8](https://peps.python.org/pep-0008/) - Python style guide
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Tweepy Docs](https://docs.tweepy.org/)
- [Gemini API](https://ai.google.dev/docs)
- [Event Registry](https://eventregistry.org/documentation)

---

*Follow these guidelines to maintain code quality and consistency.*
