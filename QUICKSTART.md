# Quick Start Guide - SHA256 News Bot

Get your Bitcoin Mining News Aggregator Bot up and running in minutes!

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your API Keys

You'll need:

1. **Google Gemini API Key**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

2. **EventRegistry API Key**
   - Sign up at [EventRegistry](https://eventregistry.org/)
   - Navigate to your account settings
   - Copy your API key

3. **Twitter API Keys**
   - Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   - Create a new app or use existing
   - Get: API Key, API Secret, Bearer Token, Access Token, Access Token Secret

4. **GitHub Personal Access Token**
   - Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
   - Generate new token (classic)
   - Give it `repo` scope
   - Copy the token

### Step 2: Configure GitHub Secrets

Go to your repository: `Settings` > `Secrets and variables` > `Actions` > `New repository secret`

Add these secrets:

| Secret Name | Description |
|-------------|-------------|
| `GOOGLE_API_KEY` | Your Google Gemini API key |
| `EVENT_REGISTRY_API_KEY` | Your EventRegistry API key |
| `GEMINI_MODEL` | `gemini-pro` (or your preferred model) |
| `TWITTER_BEARER_TOKEN` | Twitter API v2 Bearer Token |
| `TWITTER_API_KEY` | Twitter API Key (Consumer Key) |
| `TWITTER_API_SECRET` | Twitter API Secret (Consumer Secret) |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token |
| `TWITTER_ACCESS_SECRET` | Twitter Access Token Secret |
| `TWITTER_USERNAME` | Your Twitter handle (e.g., `SHA256News`) |
| `GH_PAT` | Your GitHub Personal Access Token |
| `IMAGE_LIBRARY_ACTIVE` | `True` or `False` (enable/disable images) |

### Step 3: Enable GitHub Actions

1. Go to the `Actions` tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"
3. The workflows are now active!

### Step 4: Set Up GitHub Pages

1. Go to `Settings` > `Pages`
2. Under "Source", select `Deploy from a branch`
3. Select your main branch (typically `main` or `master`) and the `/gh-pages` folder
4. Click `Save`
5. Your site will be live at `https://[username].github.io/[repo-name]/` (it may take a few minutes to deploy)

### Step 5: Test It!

1. Go to `Actions` tab
2. Select "Bitcoin Mining News Bot" workflow
3. Click "Run workflow" > "Run workflow"
4. Watch it run!
5. Check the logs to see your bot in action

## 📋 What Happens Next?

### Automatic Execution

Your bot will now run:
- **Every 2 hours**: Fetch articles, filter them, publish 1 tweet
- **Daily at 6 PM UTC**: Generate and publish daily brief

### Manual Execution

You can trigger workflows manually anytime:
- Go to Actions tab
- Select a workflow
- Click "Run workflow"

## 🎨 Customization

### Add Company Logos

1. Add PNG files to `images/company_logos/`
   - Example: `marathon_logo.png`, `riot_logo.png`
   - Note: Only PNG format is currently supported
2. Update `COMPANY_LOGO_MAP` in `bitcoin_miner_bot/image_manager.py`

### Add More Conceptual Images

1. Add PNG files to `images/conceptual/`
2. Update `CONCEPTUAL_IMAGES` list in `bitcoin_miner_bot/image_manager.py`

### Adjust Filtering

Edit the semantic filtering criteria in:
- `bitcoin_miner_bot/gemini_interface.py`
- Function: `semantically_filter_article()`

### Customize Tweet Format

Edit the tweet generation prompt in:
- `bitcoin_miner_bot/gemini_interface.py`
- Function: `generate_tweet_content()`

## 🔍 Monitoring

### Check Bot Status

1. **GitHub Actions**: Check workflow runs for success/failure
2. **Bot Logs**: Download `bot.log` artifact from failed runs
3. **Website**: Visit your GitHub Pages site to see live updates
4. **Twitter**: Check your Twitter account for published tweets

### Common Issues

#### Bot Not Tweeting?
- Verify all secrets are set correctly
- Check Twitter API rate limits
- Review `bot.log` in Actions artifacts

#### No Articles Found?
- Verify EventRegistry API key is valid
- Check your API quota
- Try different time ranges

#### Images Not Working?
- Set `IMAGE_LIBRARY_ACTIVE` secret to `True`
- Ensure image files exist in `images/` directories
- Check file permissions

## 📊 Understanding State

The bot maintains state in `bot_state.json`:
- Prevents duplicate tweets
- Tracks processed articles
- Manages article queue
- Remembers last run time

This file is automatically managed and persisted to GitHub.

## 🔒 Security Checklist

- [x] All API keys are stored in GitHub Secrets
- [x] `.env` file is in `.gitignore`
- [x] Never commit `.env` file
- [x] GH_PAT has minimal required scope (`repo`)
- [x] Regularly rotate API keys

## 📚 Learn More

- [Full README](README.md) - Comprehensive documentation
- [Model Context Protocol](MODEL_CONTEXT_PROTOCOL.md) - AI integration details
- [Copilot Instructions](copilot_instructions.md) - Development guidelines

## 🆘 Getting Help

If you encounter issues:

1. Check GitHub Actions logs
2. Review [README.md](README.md) troubleshooting section
3. Check bot.log artifact
4. Open an issue in the repository

## 🎉 Success!

Once everything is set up:

✅ Your bot fetches Bitcoin mining news every 2 hours
✅ AI filters articles for relevance
✅ Tweets are published automatically with images
✅ Daily briefs are generated at 6 PM UTC
✅ Your website shows latest updates

**Happy mining! ⛏️**

---

Follow us on Twitter: [@SHA256News](https://twitter.com/SHA256News)
