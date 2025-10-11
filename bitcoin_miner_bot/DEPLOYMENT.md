# Deployment Guide - Bitcoin Mining News Bot

This guide walks through deploying and configuring the Bitcoin mining news aggregator bot.

## Prerequisites

Before deploying, ensure you have:

### API Credentials

1. **Twitter API v2** (Developer Portal: https://developer.twitter.com/)
   - API Key and Secret
   - Access Token and Secret
   - Bearer Token
   - OAuth 1.0a enabled

2. **Google Gemini AI** (https://ai.google.dev/)
   - API Key with Gemini Pro access

3. **Event Registry** (https://eventregistry.org/)
   - API Key (free tier available)

4. **GitHub Personal Access Token**
   - Token with `repo` scope
   - For state persistence and GitHub Pages

## Local Development Setup

### 1. Clone and Setup

```bash
git clone https://github.com/SHA256-news/fantastic-couscous.git
cd fantastic-couscous/bitcoin_miner_bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Event Registry API Key
EVENT_REGISTRY_API_KEY=your_event_registry_api_key_here

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=your_username/fantastic-couscous
```

### 4. Test Locally

```bash
# Test structure
python test_structure.py

# Test with mock data
python test_mock_data.py

# Run bot once (requires API credentials)
python main.py
```

## GitHub Actions Setup

### 1. Configure Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `GEMINI_API_KEY`
- `EVENT_REGISTRY_API_KEY`

Note: `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### 2. Enable GitHub Actions

1. Go to Actions tab in your repository
2. Enable workflows if prompted
3. Workflows will run on schedule:
   - `main.yml`: Every 4 hours
   - `publish_brief.yml`: Daily at 8 AM UTC

### 3. Manual Workflow Trigger

Test workflows manually:

1. Go to Actions tab
2. Select workflow (Bitcoin Mining News Bot or Publish Daily Brief)
3. Click "Run workflow"
4. Select branch and click "Run workflow"

## GitHub Pages Setup

### 1. Enable GitHub Pages

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (will be created by workflow)
4. Folder: `/ (root)`
5. Click Save

### 2. Access Website

After first deployment, your site will be available at:
```
https://[username].github.io/fantastic-couscous/
```

### 3. Custom Domain (Optional)

1. Add CNAME file to `gh-pages/` directory
2. Configure DNS settings
3. Enable HTTPS in GitHub Pages settings

## Image Assets

### Adding Company Logos

1. Place logo PNG files in `images/company_logos/`
2. Use lowercase, underscored names: `bitmain.png`, `microbt.png`
3. Update `image_manager.py` mappings if needed

### Adding Conceptual Images

1. Place images in `images/conceptual/`
2. Update `image_manager.py` topic mappings

Recommended images:
- `bitcoin_logo.png` (default)
- `default_mining_concept.png`
- `mining_farm_generic.png`
- `asic_miner.png`
- `hashrate_chart.png`

## Monitoring and Maintenance

### Check Bot Status

1. **GitHub Actions**: View workflow runs in Actions tab
2. **Logs**: Download artifacts from workflow runs
3. **Bot State**: Check `bot_state.json` file
4. **Website**: Visit GitHub Pages URL

### Common Issues

#### No Articles Fetched
- Verify Event Registry API key
- Check API quota usage
- Review logs for errors

#### Twitter Publishing Fails
- Check Twitter API rate limits (300 tweets/3 hours)
- Verify OAuth credentials
- Review tweet character length

#### Gemini Errors
- Verify API key validity
- Check quota limits
- Review input text length

#### State Not Persisting
- Check GitHub token permissions
- Verify repository name format
- Review GitHub API rate limits

### Regular Maintenance

**Weekly:**
- Review published content quality
- Check API usage and quotas
- Monitor GitHub Actions runs

**Monthly:**
- Update dependencies: `pip install -U -r requirements.txt`
- Review and archive old logs
- Audit bot state file size

**As Needed:**
- Add new company logos
- Update image mappings
- Adjust Gemini prompts
- Modify tweet formatting

## Scaling and Optimization

### Processing More Articles

Edit `main.py`:
```python
articles_to_process = min(10, len(queue))  # Change from 5 to 10
```

### Adjusting Run Frequency

Edit `.github/workflows/main.yml`:
```yaml
schedule:
  - cron: '0 */2 * * *'  # Change from 4 to 2 hours
```

### Rate Limit Management

Twitter limits:
- 300 tweets per 3 hours (app)
- 50 tweets per 24 hours (user)

Current bot processes ~5 articles every 4 hours = ~30 tweets/day

## Troubleshooting

### Test Individual Components

```bash
# Test news fetching
python -c "from news_processor import NewsProcessor; n = NewsProcessor(); articles = n.fetch_articles(3); print(f'Fetched {len(articles)} articles')"

# Test Gemini
python -c "from gemini_interface import GeminiInterface; g = GeminiInterface(); print(g.generate_tweet_content({'title': 'Test Article', 'body': 'Test content about Bitcoin mining.'}))"

# Test Twitter (read-only)
python -c "from twitter_publisher import TwitterPublisher; t = TwitterPublisher(); print('Twitter client initialized' if t.client else 'Twitter not configured')"

# Test state management
python -c "from github_manager import GitHubManager; g = GitHubManager(); state = g.load_state(); print(f'State loaded: version {state[\"version\"]}')"
```

### Enable Debug Logging

Edit `.env`:
```env
LOG_LEVEL=DEBUG
```

### Reset Bot State

```bash
rm bot_state.json
# Bot will recreate with default state on next run
```

## Production Checklist

Before going live:

- [ ] All API credentials configured
- [ ] GitHub secrets set
- [ ] GitHub Actions enabled
- [ ] GitHub Pages activated
- [ ] Test workflows run successfully
- [ ] Local tests pass
- [ ] Company logos added (if available)
- [ ] README.md updated with repo-specific info
- [ ] Rate limits understood
- [ ] Monitoring plan in place

## Support and Resources

- **Documentation**: See `README.md` and `MODEL_CONTEXT_PROTOCOL.md`
- **Issues**: https://github.com/SHA256-news/fantastic-couscous/issues
- **Twitter API Docs**: https://developer.twitter.com/en/docs
- **Gemini API Docs**: https://ai.google.dev/docs
- **Event Registry Docs**: https://eventregistry.org/documentation

## License

MIT License - See LICENSE file for details

---

*Last updated: 2025-10-11*
