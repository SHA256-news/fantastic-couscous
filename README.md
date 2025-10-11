# Bitcoin Mining News Aggregator Bot

An intelligent Twitter bot that automatically discovers, filters, and publishes Bitcoin mining news using AI-powered content curation.

## 🚀 Features

- **Intelligent Filtering**: Uses Google Gemini AI to semantically filter articles for Bitcoin-only mining relevance
- **Automated Publishing**: Tweets news every 90 minutes using a Last-In-First-Out (LIFO) queue
- **AI-Generated Content**: Creates engaging headlines and summaries optimized for Twitter
- **Daily Briefs**: Generates comprehensive daily mining reports and publishes them as GitHub Issues
- **GitHub Pages Integration**: Automatically publishes approved briefs to a public website
- **Persistent State**: Maintains queue and history across GitHub Actions runs

## 📋 Requirements

- Python 3.11+
- Twitter Developer Account with API v2 access
- Google Gemini API key
- EventRegistry API key
- GitHub Personal Access Token (PAT) with `repo` scope

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/SHA256-news/fantastic-couscous.git
cd fantastic-couscous/bitcoin_miner_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

## 🔑 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `GOOGLE_API_KEY` - Google Gemini API key for AI filtering and content generation
- `EVENT_REGISTRY_API_KEY` - EventRegistry API key for news fetching
- `TWITTER_BEARER_TOKEN` - Twitter API v2 bearer token
- `TWITTER_API_KEY` - Twitter API key
- `TWITTER_API_SECRET` - Twitter API secret
- `TWITTER_ACCESS_TOKEN` - Twitter access token
- `TWITTER_ACCESS_SECRET` - Twitter access token secret
- `GH_PAT` - GitHub Personal Access Token (for Actions)

### GitHub Secrets

For automated deployment, add these secrets to your GitHub repository:
- `GOOGLE_API_KEY`
- `EVENT_REGISTRY_API_KEY`
- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `GH_PAT`

## 🏃 Usage

### Local Testing

Run the bot manually:
```bash
cd bitcoin_miner_bot
python main.py
```

### Automated Deployment

The bot runs automatically via GitHub Actions:

1. **Main Workflow** (`.github/workflows/main.yml`): Runs every hour to fetch news, process articles, and publish tweets
2. **Publish Brief Workflow** (`.github/workflows/publish_brief.yml`): Triggered when a daily brief issue is closed, publishing to GitHub Pages

## 📁 Project Structure

```
bitcoin_miner_bot/
├── main.py                      # Main entry point
├── news_processor.py            # News fetching and processing
├── gemini_interface.py          # AI filtering and generation
├── twitter_publisher.py         # Twitter integration
├── image_manager.py             # Image selection and management
├── daily_brief_generator.py    # Daily brief creation
├── github_manager.py            # State persistence and GitHub API
├── bot_state.json              # Persistent state file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── MODEL_CONTEXT_PROTOCOL.md  # AI model documentation
├── copilot_instructions.md    # Development guidelines
└── images/                    # Image assets
    ├── bitcoin_logo.png
    ├── default_mining_concept.png
    └── company_logos/         # Company logo directory
```

## 🤖 How It Works

### Article Processing Flow

1. **Fetch**: Retrieves articles from EventRegistry using Bitcoin mining keywords
2. **Scrape**: Extracts full article content from URLs
3. **Filter**: Uses Gemini AI to semantically determine Bitcoin mining relevance
4. **Queue**: Adds relevant articles to LIFO queue (newest first)
5. **Generate**: Creates tweet content with AI when publishing
6. **Publish**: Posts to Twitter with appropriate images
7. **Track**: Maintains published article history to avoid duplicates

### Daily Brief Generation

1. **Collect**: Gathers relevant articles throughout the day
2. **Analyze**: Generates comprehensive brief when threshold met (5+ articles)
3. **Review**: Creates GitHub Issue for human review
4. **Publish**: On issue closure, publishes to GitHub Pages

### Queue System

- **LIFO (Last In, First Out)**: Newest articles published first
- **Deduplication**: Checks against published history
- **Persistence**: State saved to `bot_state.json` and committed to git

## 🎯 Content Guidelines

### Bitcoin-Only Focus

The bot strictly filters for:
- Bitcoin mining operations and companies
- Mining hardware (ASICs) and infrastructure
- Mining profitability and market dynamics
- Mining-related regulatory news
- Strategic pivots by mining companies (e.g., to AI/HPC)

**Excluded**:
- Other cryptocurrencies (Ethereum, Solana, etc.)
- General blockchain or DeFi topics
- NFTs or smart contracts
- Altcoin mining

### Tweet Format

- Maximum 280 characters (content + URL)
- Catchy headline with no punctuation (except question marks)
- 3-point bullet summary
- Bitcoin-only language (no "crypto")
- Ethical journalism standards

## 📊 Monitoring

Check bot health via:
- GitHub Actions logs for execution details
- `bot_state.json` for queue and history
- Twitter account for published tweets
- GitHub Issues for daily briefs

## 🛡️ Error Handling

The bot includes comprehensive error handling:
- API failures default to safe behaviors
- Errors logged with DEBUG prefix
- Failed tweets return articles to queue
- State persistence even on partial failures

## 📝 Development

See `copilot_instructions.md` for detailed development guidelines and `MODEL_CONTEXT_PROTOCOL.md` for AI model interaction documentation.

### Adding Features

1. Follow existing code patterns
2. Add type hints and docstrings
3. Include error handling
4. Update documentation
5. Test with sample data

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- EventRegistry for news aggregation
- Google Gemini for AI capabilities
- Twitter API for publishing platform
- GitHub for hosting and automation

## 📞 Support

For issues or questions:
1. Check the documentation in this README
2. Review `copilot_instructions.md` for development details
3. Open a GitHub Issue with detailed information

---

**Note**: This bot is designed for Bitcoin mining news aggregation. Always ensure API keys are kept secure and never committed to the repository.