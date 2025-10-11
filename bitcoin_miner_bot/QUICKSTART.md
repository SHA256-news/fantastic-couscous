# Quick Start Guide - Bitcoin Mining News Bot

Get your Bitcoin mining news bot up and running in 10 minutes!

## Step 1: Get API Keys

### Twitter API (Required)
1. Go to https://developer.twitter.com/
2. Create a new App
3. Enable OAuth 1.0a with Read & Write permissions
4. Generate API Keys and Access Tokens
5. Save these values:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret
   - Bearer Token

### Google Gemini (Required)
1. Go to https://ai.google.dev/
2. Get an API key
3. Enable Gemini Pro model

### Event Registry (Required)
1. Go to https://eventregistry.org/
2. Sign up for a free account
3. Get your API key from account settings

## Step 2: Configure Your Bot

### Local Configuration

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SHA256-news/fantastic-couscous.git
   cd fantastic-couscous/bitcoin_miner_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create configuration file**:
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` file** and add your API keys:
   ```env
   TWITTER_API_KEY=your_twitter_api_key
   TWITTER_API_SECRET=your_twitter_api_secret
   TWITTER_ACCESS_TOKEN=your_twitter_access_token
   TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
   TWITTER_BEARER_TOKEN=your_twitter_bearer_token
   GEMINI_API_KEY=your_gemini_api_key
   EVENT_REGISTRY_API_KEY=your_event_registry_api_key
   ```

## Step 3: Test Your Setup

### Run Structure Tests
```bash
python test_structure.py
```
You should see: `✓ All tests passed! Bot structure is ready.`

### Run Mock Data Tests
```bash
python test_mock_data.py
```
You should see: `✓ All mock data tests passed!`

### Test with Real APIs (Dry Run)
```bash
python -c "
from news_processor import NewsProcessor
from gemini_interface import GeminiInterface

# Test news fetching
news = NewsProcessor()
articles = news.fetch_articles(max_articles=2)
print(f'✓ Fetched {len(articles)} articles')

# Test Gemini
if articles:
    gemini = GeminiInterface()
    tweet = gemini.generate_tweet_content(articles[0])
    print(f'✓ Generated tweet: {tweet[:100]}...')
"
```

## Step 4: Run Your Bot

### Single Run
```bash
python main.py
```

This will:
1. Fetch Bitcoin mining news
2. Enhance articles with AI
3. Select appropriate images
4. Generate tweets
5. Publish to Twitter (if configured)
6. Update bot state

### Check Results

- **Bot Log**: `cat bot.log`
- **State File**: `cat bot_state.json`
- **Twitter**: Check your Twitter account for published tweets

## Step 5: Set Up Automation (Optional)

### Configure GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add each secret from your `.env` file:
   - `TWITTER_API_KEY`
   - `TWITTER_API_SECRET`
   - `TWITTER_ACCESS_TOKEN`
   - `TWITTER_ACCESS_TOKEN_SECRET`
   - `TWITTER_BEARER_TOKEN`
   - `GEMINI_API_KEY`
   - `EVENT_REGISTRY_API_KEY`

### Enable GitHub Actions

1. Go to Actions tab
2. Enable workflows if prompted
3. Manually trigger first run:
   - Select "Bitcoin Mining News Bot"
   - Click "Run workflow"

### Set Up GitHub Pages

1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (created automatically)
4. Click Save

Your website will be at: `https://[username].github.io/fantastic-couscous/`

## Step 6: Add Company Logos (Optional)

Enhance tweets with company logos:

1. Get PNG logos for:
   - Bitmain
   - MicroBT
   - Marathon
   - Riot Platforms
   - Core Scientific
   - Other mining companies

2. Save them to `images/company_logos/`:
   ```bash
   cp bitmain-logo.png images/company_logos/bitmain.png
   cp microbt-logo.png images/company_logos/microbt.png
   # etc.
   ```

3. Logos will automatically be used when articles mention these companies

## Troubleshooting

### "No module named 'dotenv'"
```bash
pip install -r requirements.txt
```

### "No articles fetched"
- Check Event Registry API key is valid
- Verify you haven't exceeded API quota
- Try running again (timing may affect results)

### "Twitter publishing failed"
- Verify all Twitter credentials
- Check you have Read & Write permissions
- Ensure OAuth 1.0a is enabled

### "Gemini errors"
- Verify API key is correct
- Check you're not exceeding quota
- Ensure Gemini Pro is available in your region

## Usage Tips

### Adjusting Tweet Frequency

Edit `main.py` to change articles processed per run:
```python
articles_to_process = min(5, len(queue))  # Change 5 to desired number
```

### Customizing Tweet Style

Edit `gemini_interface.py`, method `generate_tweet_content()` to adjust the AI prompt.

### Adding More News Sources

Edit `news_processor.py` to add RSS feeds or other news sources.

### Monitoring Your Bot

```bash
# Watch logs in real-time
tail -f bot.log

# Check queue status
python -c "from github_manager import GitHubManager; g = GitHubManager(); s = g.load_state(); print(f'Queue: {len(s[\"article_queue\"])} articles')"

# View published articles
python -c "from github_manager import GitHubManager; g = GitHubManager(); s = g.load_state(); print(f'Published: {len(s[\"published_articles\"])} articles')"
```

## What's Next?

### Daily Briefs

Generate a daily brief manually:
```bash
python -c "
from daily_brief_generator import DailyBriefGenerator
from news_processor import NewsProcessor

brief_gen = DailyBriefGenerator()
news = NewsProcessor()
articles = news.fetch_articles(max_articles=20)
brief_gen.generate_brief(articles)
print('Brief generated in gh-pages/briefs/')
"
```

### Customize Website

Edit `gh-pages/index.html` to customize your website look and feel.

### Advanced Configuration

See `DEPLOYMENT.md` for advanced configuration options.

## Getting Help

- **Documentation**: See `README.md` and `MODEL_CONTEXT_PROTOCOL.md`
- **Issues**: https://github.com/SHA256-news/fantastic-couscous/issues
- **Testing**: Run `python test_structure.py` and `python test_mock_data.py`

## Success Checklist

- [ ] API keys obtained and configured
- [ ] Dependencies installed
- [ ] Structure tests pass
- [ ] Mock data tests pass
- [ ] Bot runs successfully locally
- [ ] Tweets published to Twitter
- [ ] GitHub Actions configured (if using automation)
- [ ] GitHub Pages enabled (if using website)
- [ ] Company logos added (optional)
- [ ] Bot running smoothly

## Example Output

When running successfully, you'll see:
```
2025-10-11 19:00:00,000 - main - INFO - === Bot Run Started ===
2025-10-11 19:00:05,123 - news_processor - INFO - Fetched 15 new articles
2025-10-11 19:00:10,456 - gemini_interface - INFO - Enhanced article: Bitcoin Mining...
2025-10-11 19:00:15,789 - twitter_publisher - INFO - Tweet published successfully: 123456789
2025-10-11 19:00:20,012 - main - INFO - === Bot Run Complete - Processed 5 articles ===
```

🎉 **Congratulations!** Your Bitcoin mining news bot is now operational!

---

*For more detailed information, see the full documentation in `README.md` and `DEPLOYMENT.md`.*
