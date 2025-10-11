# Setup Guide for Bitcoin Mining News Aggregator Bot

This guide will help you set up and deploy the Bitcoin Mining News Aggregator Bot.

## Prerequisites

1. **Twitter Developer Account**
   - Apply at https://developer.twitter.com/
   - Create an app and get API credentials (v2 with OAuth 1.0a)

2. **Google Gemini API Key**
   - Sign up at https://makersuite.google.com/
   - Create an API key for Gemini Pro

3. **EventRegistry API Key**
   - Register at https://eventregistry.org/
   - Get an API key (free tier available)

4. **GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Create a token with `repo` scope

## Local Setup

### 1. Clone and Install

```bash
git clone https://github.com/SHA256-news/fantastic-couscous.git
cd fantastic-couscous/bitcoin_miner_bot
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your API keys:

```bash
GOOGLE_API_KEY="your_gemini_api_key_here"
EVENT_REGISTRY_API_KEY="your_eventregistry_api_key_here"
TWITTER_BEARER_TOKEN="your_twitter_bearer_token_here"
TWITTER_API_KEY="your_twitter_api_key_here"
TWITTER_API_SECRET="your_twitter_api_secret_here"
TWITTER_ACCESS_TOKEN="your_twitter_access_token_here"
TWITTER_ACCESS_SECRET="your_twitter_access_secret_here"
GH_PAT="your_github_pat_here"
```

### 3. Test Locally

```bash
# Run the test suite
python test_bot.py

# Run the bot once
python main.py
```

## GitHub Actions Deployment

### 1. Add Secrets to Repository

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:
- `GOOGLE_API_KEY`
- `EVENT_REGISTRY_API_KEY`
- `TWITTER_BEARER_TOKEN`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`
- `GH_PAT`

### 2. Enable GitHub Actions

1. Go to Actions tab in your repository
2. Enable workflows if prompted
3. The workflows will run automatically on schedule

### 3. Configure GitHub Pages

1. Go to Settings → Pages
2. Source: "GitHub Actions"
3. The daily briefs will be published to your GitHub Pages site

## Workflow Schedule

### Main Workflow (`main.yml`)
- **Trigger**: Runs every hour (adjust cron for 90-minute intervals)
- **Purpose**: Fetches news, filters articles, publishes tweets, generates daily briefs

### Publish Brief Workflow (`publish_brief.yml`)
- **Trigger**: When a daily brief issue is closed
- **Purpose**: Publishes the approved brief to GitHub Pages

## Usage

### Manual Workflow Trigger

You can manually trigger the bot from GitHub Actions:
1. Go to Actions → "Bitcoin Mining News Bot"
2. Click "Run workflow"
3. Select branch and click "Run workflow"

### Daily Brief Review Process

1. Bot generates a daily brief (when ≥5 articles collected)
2. Creates a GitHub Issue with label `daily-brief`
3. Review the content in the issue
4. Close the issue to approve and publish to GitHub Pages

### Monitoring

- **State File**: Check `bot_state.json` for queue status
- **GitHub Actions Logs**: View detailed execution logs
- **Twitter Account**: Monitor published tweets
- **GitHub Issues**: Review daily briefs

## Customization

### Adjust Publication Frequency

Edit `.github/workflows/main.yml`:

```yaml
on:
  schedule:
    - cron: '0 */1 * * *'  # Every hour
    # For 90 minutes: '*/90 * * * *' (if supported)
    # Or use: '0,30 */1 * * *' for every 30 minutes
```

### Modify Bitcoin Mining Keywords

Edit `news_processor.py`:

```python
BITCOIN_MINING_KEYWORDS = [
    "bitcoin mining",
    # Add your keywords
]

MINING_COMPANIES = [
    "Marathon Digital",
    # Add your companies
]
```

### Adjust AI Prompts

Edit `gemini_interface.py` to customize:
- Semantic filtering criteria
- Tweet generation style
- Content guidelines

## Troubleshooting

### Bot Not Publishing Tweets

1. Check Twitter API credentials in GitHub Secrets
2. Verify Twitter API rate limits
3. Check GitHub Actions logs for errors
4. Ensure `bot_state.json` has articles in queue

### No Articles Found

1. Verify EventRegistry API key is valid
2. Check if keywords are too restrictive
3. Review filtering logic in `news_processor.py`
4. Test with broader date ranges

### Daily Brief Not Generated

1. Ensure at least 5 articles are collected
2. Check that `last_brief_date` is not today
3. Verify Gemini API key and quota
4. Review `daily_brief_generator.py` logic

### GitHub Pages Not Publishing

1. Enable GitHub Pages in repository settings
2. Ensure `publish_brief.yml` workflow is enabled
3. Check that issue has `daily-brief` label
4. Review workflow logs for errors

## Best Practices

1. **Rate Limiting**: Be mindful of API rate limits
   - EventRegistry: ~1000 requests/day (free tier)
   - Twitter: 50 tweets per 24 hours (standard)
   - Gemini: Check your quota

2. **Content Quality**: Review published tweets regularly
   - Adjust AI prompts if needed
   - Update filtering criteria
   - Monitor false positives/negatives

3. **State Management**: 
   - Don't manually edit `bot_state.json` while bot is running
   - Backup state file before major changes
   - Monitor queue size (keep under 100 articles)

4. **Security**:
   - Never commit `.env` file
   - Rotate API keys periodically
   - Use GitHub Secrets for sensitive data
   - Review published content for accuracy

## Support

For issues or questions:
1. Check this setup guide
2. Review `copilot_instructions.md` for development details
3. Check `MODEL_CONTEXT_PROTOCOL.md` for AI model info
4. Open a GitHub Issue with detailed information

## License

This project is open source and available under the MIT License.
