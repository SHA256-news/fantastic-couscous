# SHA256 News - Bitcoin Mining News Aggregator Bot

An intelligent, automated Twitter bot that aggregates, filters, and publishes Bitcoin mining news using AI-powered content analysis.

## 🌟 Features

- **AI-Powered Filtering**: Uses Google Gemini to semantically filter articles for Bitcoin mining relevance
- **Smart Content Generation**: Automatically generates engaging tweet content with headlines and 3-point summaries
- **Intelligent Image Selection**: Matches company logos or conceptual images to articles
- **LIFO Queue Management**: Prioritizes most recent news for maximum relevance
- **Daily Briefs**: Comprehensive daily summaries with thematic trend analysis
- **GitHub Pages Integration**: Dynamic website with latest headlines and briefs
- **State Persistence**: Robust state management across runs
- **Deduplication**: Prevents duplicate articles using URL and event URI tracking

## 🏗️ Architecture

```
bitcoin_miner_bot/
├── main.py                    # Main orchestrator
├── news_processor.py          # EventRegistry integration & content fetching
├── gemini_interface.py        # AI filtering & content generation
├── twitter_publisher.py       # Tweet publishing with media
├── image_manager.py           # Image selection and management
├── daily_brief_generator.py   # Daily brief creation
├── github_manager.py          # State persistence & GitHub Pages updates
└── daily_brief_script.py      # Daily brief publication script

.github/workflows/
├── main.yml                   # Main bot workflow (every 2 hours)
└── publish_brief.yml          # Daily brief workflow (daily at 6 PM UTC)

gh-pages/
├── index.html                 # Main website
├── sha256news-tweets.json     # Latest tweets data
├── briefs_index.json          # Briefs index
└── briefs/                    # Individual brief HTML files

images/
├── company_logos/             # Company-specific logos
└── conceptual/                # Generic mining images
```

## 🚀 Setup

### Prerequisites

- Python 3.11+
- GitHub account with repository
- Google Gemini API key
- EventRegistry API key
- Twitter Developer account with API keys
- GitHub Personal Access Token (PAT) with `repo` scope

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SHA256-news/fantastic-couscous.git
   cd fantastic-couscous
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and fill in your API keys
   ```

4. **Run the bot locally**
   ```bash
   python -m bitcoin_miner_bot.main
   ```

### GitHub Actions Setup

1. **Set up GitHub Secrets**
   
   Go to your repository's Settings > Secrets and variables > Actions, and add:
   
   - `GOOGLE_API_KEY` - Your Google Gemini API key
   - `EVENT_REGISTRY_API_KEY` - Your EventRegistry API key
   - `GEMINI_MODEL` - Model name (e.g., "gemini-pro")
   - `TWITTER_BEARER_TOKEN` - Twitter API v2 bearer token
   - `TWITTER_API_KEY` - Twitter API key
   - `TWITTER_API_SECRET` - Twitter API secret
   - `TWITTER_ACCESS_TOKEN` - Twitter access token
   - `TWITTER_ACCESS_SECRET` - Twitter access token secret
   - `TWITTER_USERNAME` - Your Twitter handle (e.g., "SHA256News")
   - `GH_PAT` - GitHub Personal Access Token with `repo` scope
   - `IMAGE_LIBRARY_ACTIVE` - "True" or "False" to enable/disable images

2. **Enable GitHub Actions**
   
   GitHub Actions should start running automatically based on the schedules:
   - Main bot: Every 2 hours
   - Daily brief: Daily at 6 PM UTC

3. **Set up GitHub Pages**
   
   Go to Settings > Pages and configure:
   - Source: Deploy from a branch
   - Branch: Select a branch that contains the `gh-pages/` directory

## 📖 Usage

### Automated Operation

The bot runs automatically via GitHub Actions:
- **Every 2 hours**: Fetches new articles, filters them, and publishes 1 tweet
- **Daily at 6 PM UTC**: Generates and publishes a comprehensive daily brief

### Manual Execution

Trigger workflows manually from the Actions tab:
- "Bitcoin Mining News Bot" - Run main bot cycle
- "Publish Daily Brief" - Generate daily brief

### Local Testing

```bash
# Run main bot
python -m bitcoin_miner_bot.main

# Generate daily brief
python -m bitcoin_miner_bot.daily_brief_script
```

## 🎨 Customization

### Adding Company Logos

1. Add PNG files to `images/company_logos/`
2. Update `COMPANY_LOGO_MAP` in `bitcoin_miner_bot/image_manager.py`

### Adding Conceptual Images

1. Add PNG files to `images/conceptual/`
2. Update `CONCEPTUAL_IMAGES` list in `bitcoin_miner_bot/image_manager.py`

### Adjusting Filter Criteria

Edit the semantic filtering prompt in `bitcoin_miner_bot/gemini_interface.py`'s `semantically_filter_article()` function.

### Modifying Tweet Format

Adjust the tweet generation prompt in `bitcoin_miner_bot/gemini_interface.py`'s `generate_tweet_content()` function.

## 📊 State Management

The bot maintains state in `bot_state.json`:
- `processed_urls`: URLs that have been tweeted
- `processed_event_uris`: EventRegistry URIs for story deduplication
- `daily_brief_urls`: URLs collected for today's brief
- `lifo_queue`: Queue of articles waiting to be tweeted
- `last_run`: Timestamp of last execution
- `last_brief_date`: Date of last brief publication

State is automatically persisted to GitHub after each run.

## 🔒 Security

- **Never commit `.env` file** - It contains sensitive API keys
- **Use GitHub Secrets** for all credentials in Actions
- **Rotate API keys** periodically
- **Review GH_PAT permissions** - Only grant necessary scopes

## 🛠️ Troubleshooting

### Bot not tweeting?

- Check GitHub Actions logs
- Verify all secrets are set correctly
- Ensure Twitter API rate limits aren't exceeded
- Check `bot.log` for errors

### No articles being found?

- Verify EventRegistry API key is valid
- Check EventRegistry query parameters
- Review semantic filtering criteria

### Images not attaching?

- Ensure `IMAGE_LIBRARY_ACTIVE` is set to "True"
- Verify image files exist in `images/` directories
- Check file permissions

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Contact

Follow us on Twitter: [@SHA256News](https://twitter.com/SHA256News)

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- EventRegistry for news aggregation
- Twitter API for social media integration
- GitHub Pages for hosting

---

**Built with ⛏️ for the Bitcoin mining community**