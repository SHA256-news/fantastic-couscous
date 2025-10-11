# GitHub Copilot Instructions

## Project Context
This is a Bitcoin-Only Mining News Aggregator Bot that automatically fetches, filters, and publishes Bitcoin mining news to Twitter, while generating comprehensive daily briefs.

## Code Style and Conventions

### Python Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Docstrings for all public functions (Google style)
- Descriptive variable names (no single letters except in loops)
- Maximum line length: 100 characters

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private methods: `_leading_underscore`

### Error Handling
- Use try-except blocks for external API calls
- Log errors with "DEBUG:" prefix
- Return sensible defaults on errors
- Never raise unhandled exceptions in main execution flow

### Logging
- Use print statements with "DEBUG:" prefix
- Log important state changes
- Log API call results
- Log queue operations

## Project Structure

```
bitcoin_miner_bot/
├── main.py                      # Entry point, orchestrates all operations
├── news_processor.py            # Fetches and processes news articles
├── gemini_interface.py          # AI filtering and content generation
├── twitter_publisher.py         # Twitter API integration
├── image_manager.py             # Image selection and management
├── daily_brief_generator.py    # Daily summary generation
├── github_manager.py            # State persistence and GitHub integration
├── bot_state.json              # Persistent state (managed by git)
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variable template
```

## Key Components

### State Management
- State is stored in `bot_state.json`
- Contains: article queue, published IDs, last fetch time, brief date
- Always save state after modifications
- Use GitHubManager for all state operations

### Queue System
- LIFO (Last In, First Out) queue
- Pop from end of array for newest articles
- Check for duplicates before adding
- Keep published IDs for deduplication

### Article Processing Flow
1. Fetch from EventRegistry
2. Scrape full content
3. Filter with Gemini (semantic analysis)
4. Add to queue if relevant
5. Generate tweet content when publishing
6. Select appropriate image
7. Publish to Twitter
8. Mark as published

### Daily Brief Flow
1. Collect articles throughout the day
2. Check if conditions met (minimum 5 articles, new day)
3. Generate comprehensive brief with Gemini
4. Create GitHub issue for review
5. On issue close, publish to GitHub Pages

## Important Rules

### Bitcoin-Only Focus
- Filter for Bitcoin mining content exclusively
- No mentions of other cryptocurrencies in output
- No use of generic term "crypto"
- Focus on mining operations, hardware, companies, infrastructure

### Tweet Requirements
- Maximum 280 characters total (content + URL)
- No punctuation except question marks
- Must be engaging and specific
- No repetition of URL title info
- Include URL and optional image

### API Keys (Secrets)
Never hardcode API keys. Always use environment variables:
- `GOOGLE_API_KEY` - Gemini AI
- `EVENT_REGISTRY_API_KEY` - News source
- `TWITTER_*` - Twitter API credentials
- `GH_PAT` - GitHub personal access token

### Testing
- Test with small batches first
- Verify state persistence
- Check queue LIFO behavior
- Test error handling paths
- Validate tweet character limits

## Common Tasks

### Adding a New Feature
1. Create function with type hints and docstring
2. Add error handling
3. Update state if needed
4. Add logging statements
5. Test with sample data
6. Update this documentation

### Debugging Issues
1. Check DEBUG log output
2. Verify API credentials
3. Check bot_state.json contents
4. Validate article data structure
5. Test AI prompts independently

### Modifying AI Prompts
1. Test new prompts with sample articles
2. Validate output format
3. Check character limits
4. Ensure Bitcoin-only focus maintained
5. Document changes in MODEL_CONTEXT_PROTOCOL.md

### Adding New Article Sources
1. Implement fetcher in news_processor.py
2. Ensure consistent article dictionary format
3. Add to main.py orchestration
4. Test with semantic filter
5. Update documentation

## Dependencies

### External APIs
- Google Gemini: AI filtering and generation
- EventRegistry: News article source
- Twitter: Publishing platform
- GitHub: State persistence and issue creation

### Python Packages
- google-generativeai: Gemini SDK
- tweepy: Twitter API v2
- EventRegistry: News API
- PyGithub: GitHub API
- beautifulsoup4: Web scraping
- python-dotenv: Environment variables
- requests: HTTP client

## Maintenance Notes

### State File Growth
- Keep published_articles list capped at 1000 items
- Consider archiving old daily_brief_articles
- Monitor bot_state.json file size

### API Rate Limits
- EventRegistry: Check plan limits
- Twitter: Respect rate limits (consider backoff)
- Gemini: Monitor token usage and costs
- GitHub: Use conditional requests where possible

### Monitoring
- Check GitHub Actions logs regularly
- Monitor Twitter account for publishing issues
- Review daily brief issues for quality
- Track API error rates

## Future Enhancements
- Add sentiment analysis
- Implement topic clustering
- Add company logo recognition
- Create weekly summaries
- Add email notifications
- Implement web dashboard
- Add analytics and metrics
- Support multiple languages
