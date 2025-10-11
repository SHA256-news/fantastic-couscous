# Changelog

All notable changes to the Bitcoin Mining News Aggregator Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-11

### Added
- Initial release of Bitcoin Mining News Aggregator Bot
- News fetching from EventRegistry with Bitcoin mining keywords
- AI-powered semantic filtering using Google Gemini
- Intelligent article processing with web scraping
- LIFO queue system for content selection
- Automated Twitter publishing with images
- AI-generated tweet content (headline + 3-point summary)
- Daily brief generation with comprehensive analysis
- GitHub Issues integration for brief review workflow
- GitHub Pages publishing for approved briefs
- Persistent state management via `bot_state.json`
- GitHub Actions workflows for automation
- Image management with company logo support
- Comprehensive documentation:
  - README.md with project overview
  - SETUP.md with deployment instructions
  - MODEL_CONTEXT_PROTOCOL.md for AI model guidelines
  - copilot_instructions.md for development guidelines
- Test suite for validation (`test_bot.py`)
- Environment variable configuration via `.env`
- Python package structure with proper imports

### Features
- **Smart Filtering**: Bitcoin-only focus with nuanced understanding
- **LIFO Queue**: Newest articles published first
- **Deduplication**: Tracks published articles to avoid repeats
- **Error Handling**: Graceful failures with logging
- **Rate Limiting**: Considerate of API quotas
- **Extensible**: Easy to add new features or data sources

### Technical Stack
- Python 3.11+
- Google Gemini Pro for AI
- EventRegistry for news aggregation
- Tweepy for Twitter API v2
- BeautifulSoup4 for web scraping
- PyGithub for GitHub API integration
- GitHub Actions for automation

### Documentation
- Complete README with feature overview
- Step-by-step setup guide
- API integration documentation
- Development guidelines for contributors
- Model context protocol for AI interactions

### Workflows
- `main.yml`: Hourly execution for news processing and publishing
- `publish_brief.yml`: Triggered on issue close for GitHub Pages deployment

[1.0.0]: https://github.com/SHA256-news/fantastic-couscous/releases/tag/v1.0.0
