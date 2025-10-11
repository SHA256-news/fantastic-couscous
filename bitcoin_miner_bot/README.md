# Bitcoin Mining News Aggregator Bot

An automated Twitter bot that aggregates, analyzes, and publishes Bitcoin mining news using AI-powered content enhancement.

## Features

- 🔍 **Smart News Aggregation**: Fetches Bitcoin mining news from multiple sources using Event Registry API
- 🤖 **AI Enhancement**: Uses Google Gemini AI to analyze, summarize, and enhance articles
- 🐦 **Twitter Integration**: Automatically publishes curated news to Twitter with intelligent image selection
- 📊 **Daily Briefs**: Generates comprehensive daily news briefs with trend analysis
- 🌐 **GitHub Pages Website**: Maintains a live website with latest headlines and brief archives
- 💾 **State Persistence**: Robust LIFO queue management with GitHub-based state persistence
- 🖼️ **Intelligent Images**: Matches company logos and conceptual images to articles

## Architecture

### Core Modules

- **`main.py`**: Main orchestrator and entry point
- **`news_processor.py`**: Handles news fetching and content extraction
- **`gemini_interface.py`**: AI-powered content analysis and generation
- **`twitter_publisher.py`**: Twitter API integration for publishing
- **`image_manager.py`**: Intelligent image selection logic
- **`daily_brief_generator.py`**: Daily summary generation
- **`github_manager.py`**: State persistence and GitHub Pages management

### Workflows

- **`main.yml`**: Runs every 4 hours to fetch and publish news
- **`publish_brief.yml`**: Generates daily briefs at 8 AM UTC

## Setup

### Prerequisites

- Python 3.11+
- Twitter API credentials (v2 with OAuth 1.0a)
- Google Gemini API key
- Event Registry API key
- GitHub repository with Actions enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SHA256-news/fantastic-couscous.git
cd fantastic-couscous/bitcoin_miner_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API credentials
```

### Configuration

Create a `.env` file based on `.env.example`:

```env
# Twitter API Credentials
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# Gemini API Key
GEMINI_API_KEY=your_gemini_key

# Event Registry API Key
EVENT_REGISTRY_API_KEY=your_event_registry_key

# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_REPO=username/repo
```

### GitHub Secrets

Configure the following secrets in your GitHub repository:

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `GEMINI_API_KEY`
- `EVENT_REGISTRY_API_KEY`

## Usage

### Manual Execution

Run the bot manually:
```bash
cd bitcoin_miner_bot
python main.py
```

Generate a daily brief:
```bash
python -c "from daily_brief_generator import DailyBriefGenerator; from news_processor import NewsProcessor; brief_gen = DailyBriefGenerator(); news = NewsProcessor(); articles = news.fetch_articles(50); brief_gen.generate_brief(articles)"
```

### Automated Execution

The bot runs automatically via GitHub Actions:
- **Every 4 hours**: Fetches and publishes news
- **Daily at 8 AM UTC**: Generates daily brief

## Directory Structure

```
bitcoin_miner_bot/
├── main.py                     # Main entry point
├── news_processor.py           # News fetching
├── gemini_interface.py         # AI integration
├── twitter_publisher.py        # Twitter publishing
├── image_manager.py            # Image selection
├── daily_brief_generator.py    # Brief generation
├── github_manager.py           # GitHub integration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── bot_state.json             # Bot state (generated)
├── bot.log                    # Log file (generated)
├── .github/
│   └── workflows/
│       ├── main.yml           # Main bot workflow
│       └── publish_brief.yml  # Daily brief workflow
├── images/
│   ├── company_logos/         # Company logo PNGs
│   └── conceptual/            # Conceptual images
│       ├── bitcoin_logo.png
│       ├── default_mining_concept.png
│       └── mining_farm_generic.png
└── gh-pages/                  # GitHub Pages content
    ├── index.html             # Main website
    ├── brief_template.html    # Brief template
    ├── sha256news-tweets.json # Latest tweets
    ├── briefs_index.json      # Briefs index
    └── briefs/                # Individual briefs
```

## How It Works

### News Processing Pipeline

1. **Fetch Articles**: Retrieves Bitcoin mining news from Event Registry API
2. **Content Extraction**: Scrapes full article content from source URLs
3. **AI Enhancement**: Gemini analyzes and summarizes each article
4. **Queue Management**: Articles stored in LIFO queue for processing
5. **Image Selection**: Matches appropriate images (company logos or conceptual)
6. **Tweet Generation**: AI generates engaging tweet content
7. **Publication**: Posts to Twitter with selected image
8. **State Persistence**: Updates bot state and GitHub Pages data

### Daily Brief Generation

1. **Article Collection**: Gathers all articles from the last 24 hours
2. **Trend Analysis**: Gemini identifies themes and trends
3. **Content Generation**: Creates structured brief with sections
4. **HTML Output**: Generates formatted HTML page
5. **Index Update**: Updates website with latest brief
6. **GitHub Pages**: Deploys to live website

## Image Management

The bot intelligently selects images based on article content:

### Company Logos
Place company logo PNGs in `images/company_logos/`:
- `bitmain.png`, `microbt.png`, `riot.png`, etc.
- Automatically matched to company mentions in articles

### Conceptual Images
Generic mining-related images in `images/conceptual/`:
- `bitcoin_logo.png` (default)
- `default_mining_concept.png`
- `mining_farm_generic.png`

## Logging

Comprehensive logging to both file and console:
- **Log File**: `bot.log`
- **Log Level**: Configurable via `LOG_LEVEL` env variable
- **Format**: Timestamp, module, level, message

## State Management

Bot state is persisted in `bot_state.json`:
```json
{
  "version": "1.0",
  "last_run": "2024-01-01T12:00:00",
  "article_queue": [...],
  "published_articles": [...],
  "daily_briefs": [...]
}
```

## GitHub Pages

The bot maintains a live website at `https://username.github.io/repo-name/`:
- **Homepage**: Latest headlines and daily brief
- **Brief Archive**: Historical daily briefs
- **Dynamic Updates**: Real-time content from JSON feeds

## Troubleshooting

### No articles fetched
- Check Event Registry API key
- Verify API quota hasn't been exceeded
- Check network connectivity

### Twitter publishing fails
- Verify Twitter API credentials
- Check rate limits (300 tweets per 3 hours)
- Ensure OAuth 1.0a is properly configured

### Gemini AI errors
- Check API key validity
- Verify quota limits
- Review input text length (max ~2000 chars)

### State not persisting
- Check GitHub token permissions
- Verify repository name format (owner/repo)
- Review GitHub API rate limits

## Development

### Running Tests
```bash
# Test news fetching
python -c "from news_processor import NewsProcessor; n = NewsProcessor(); print(n.fetch_articles(5))"

# Test Gemini interface
python -c "from gemini_interface import GeminiInterface; g = GeminiInterface(); print(g.generate_tweet_content({'title': 'Test', 'body': 'Test body'}))"

# Test image selection
python -c "from image_manager import ImageManager; i = ImageManager(); print(i.list_available_images())"
```

### Adding New Features
1. Create feature branch
2. Implement changes with logging
3. Test locally with `.env` configuration
4. Update documentation
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## Support

For issues and questions:
- GitHub Issues: https://github.com/SHA256-news/fantastic-couscous/issues
- Documentation: See MODEL_CONTEXT_PROTOCOL.md

## Credits

- Built with Python 3.11
- Powered by Google Gemini AI
- News data from Event Registry
- Twitter API v2
- GitHub Actions & Pages
