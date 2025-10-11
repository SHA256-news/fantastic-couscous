# SHA256.news - Bitcoin Mining News Aggregator Bot

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

An intelligent, AI-powered Bitcoin mining news aggregator bot that automatically fetches, analyzes, and publishes cryptocurrency mining news to Twitter and a dedicated website.

## 🚀 Features

- **Automated News Aggregation**: Fetches Bitcoin mining news from multiple sources
- **AI-Powered Analysis**: Uses Google Gemini AI for content enhancement and summarization
- **Twitter Integration**: Automatically publishes curated news with intelligent image selection
- **Daily Briefs**: Generates comprehensive daily summaries with trend analysis
- **GitHub Pages Website**: Live website with latest headlines and brief archives
- **Smart State Management**: LIFO queue with GitHub-based persistence
- **Intelligent Images**: Automatic company logo and conceptual image matching

## 📁 Project Structure

```
bitcoin_miner_bot/          # Main bot directory
├── main.py                 # Bot orchestrator
├── news_processor.py       # News fetching and processing
├── gemini_interface.py     # AI integration
├── twitter_publisher.py    # Twitter publishing
├── image_manager.py        # Image selection
├── daily_brief_generator.py # Brief generation
├── github_manager.py       # State and GitHub integration
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── README.md              # Detailed documentation
├── MODEL_CONTEXT_PROTOCOL.md  # Developer context
├── copilot_instructions.md    # Coding guidelines
├── .github/workflows/     # GitHub Actions
├── images/                # Image assets
└── gh-pages/              # Website content
```

## 🛠️ Quick Start

### Prerequisites

- Python 3.11 or higher
- Twitter API credentials (v2 with OAuth 1.0a)
- Google Gemini API key
- Event Registry API key
- GitHub repository with Actions enabled

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SHA256-news/fantastic-couscous.git
   cd fantastic-couscous/bitcoin_miner_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

## 🔧 Configuration

Create a `.env` file with your credentials:

```env
# Twitter API
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# Google Gemini AI
GEMINI_API_KEY=your_gemini_key

# Event Registry
EVENT_REGISTRY_API_KEY=your_event_registry_key

# GitHub (optional)
GITHUB_TOKEN=your_github_token
GITHUB_REPO=username/repo
```

### GitHub Secrets

For automated runs via GitHub Actions, configure these repository secrets:
- `TWITTER_API_KEY`, `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET`, `TWITTER_BEARER_TOKEN`
- `GEMINI_API_KEY`
- `EVENT_REGISTRY_API_KEY`

## 🤖 How It Works

1. **News Fetching**: Retrieves Bitcoin mining articles from Event Registry
2. **AI Enhancement**: Gemini analyzes and summarizes each article
3. **Queue Management**: Articles stored in LIFO queue for processing
4. **Image Selection**: Matches appropriate images (company logos or concepts)
5. **Tweet Generation**: AI creates engaging tweet content
6. **Publication**: Posts to Twitter with selected images
7. **State Persistence**: Updates bot state and GitHub Pages

## 📅 Automated Execution

The bot runs automatically via GitHub Actions:
- **Every 4 hours**: Fetches and publishes news (`main.yml`)
- **Daily at 8 AM UTC**: Generates daily brief (`publish_brief.yml`)

Manual triggers available via workflow_dispatch.

## 🌐 GitHub Pages Website

Access your live website at: `https://username.github.io/repo-name/`

Features:
- Latest headlines from Twitter
- Daily brief archive
- Trend analysis
- Mobile-responsive design

## 📚 Documentation

- **[README.md](bitcoin_miner_bot/README.md)**: Complete setup and usage guide
- **[MODEL_CONTEXT_PROTOCOL.md](bitcoin_miner_bot/MODEL_CONTEXT_PROTOCOL.md)**: Technical architecture and AI context
- **[copilot_instructions.md](bitcoin_miner_bot/copilot_instructions.md)**: Development guidelines

## 🧪 Testing

Test individual components:

```bash
# Test news fetching
python -c "from news_processor import NewsProcessor; print(NewsProcessor().fetch_articles(3))"

# Test Gemini AI
python -c "from gemini_interface import GeminiInterface; print(GeminiInterface().generate_tweet_content({'title': 'Test', 'body': 'Test'}))"

# Test image selection
python -c "from image_manager import ImageManager; print(ImageManager().list_available_images())"
```

## 🛡️ Security

- API keys stored in environment variables (never committed)
- GitHub Secrets for automated workflows
- Input validation and sanitization
- Rate limiting and error handling

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Update documentation
5. Submit a pull request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Credits

Built with:
- Python 3.11
- [Google Gemini AI](https://ai.google.dev/)
- [Event Registry](https://eventregistry.org/)
- [Tweepy](https://www.tweepy.org/)
- [GitHub Actions](https://github.com/features/actions)
- [GitHub Pages](https://pages.github.com/)

## 📧 Support

- GitHub Issues: [Report a bug](https://github.com/SHA256-news/fantastic-couscous/issues)
- Documentation: See `bitcoin_miner_bot/` directory

---

**SHA256.news** - Automated Bitcoin Mining Intelligence