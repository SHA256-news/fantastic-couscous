# Quick Start Guide

Get the Bitcoin Mining News Aggregator Bot running in 5 minutes!

## 🚀 Fastest Path to Deployment

### 1. Get API Keys (5-10 minutes)

You'll need:
- **Twitter API**: https://developer.twitter.com/en/portal/dashboard
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **EventRegistry**: https://eventregistry.org/register
- **GitHub Token**: https://github.com/settings/tokens (with `repo` scope)

### 2. Configure GitHub Secrets (2 minutes)

Go to: `Your Repo → Settings → Secrets and variables → Actions → New repository secret`

Add these 8 secrets:
```
GOOGLE_API_KEY
EVENT_REGISTRY_API_KEY
TWITTER_BEARER_TOKEN
TWITTER_API_KEY
TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_SECRET
GH_PAT
```

### 3. Enable GitHub Actions & Pages (1 minute)

**Enable Actions:**
- Go to `Actions` tab → Click "I understand my workflows, go ahead and enable them"

**Enable Pages:**
- Go to `Settings → Pages`
- Source: "GitHub Actions"
- Save

### 4. Run First Test (30 seconds)

**Manual trigger:**
- Go to `Actions → Bitcoin Mining News Bot → Run workflow`
- Click "Run workflow" button
- Wait 1-2 minutes and check the logs

### 5. Monitor (Ongoing)

**Check these regularly:**
- **Actions Logs**: See what the bot is doing
- **bot_state.json**: View queue and published articles
- **Twitter Account**: See published tweets
- **Issues Tab**: Review daily briefs (labeled `daily-brief`)
- **GitHub Pages**: Published briefs at `https://[username].github.io/[repo-name]/`

## 📊 What Happens Next?

### Hourly Cycle (Automated)
1. ✅ Fetch Bitcoin mining news from EventRegistry
2. ✅ Filter with AI for relevance (Bitcoin-only)
3. ✅ Add relevant articles to queue
4. ✅ Publish 1 tweet from queue (newest first - LIFO)
5. ✅ Generate daily brief when 5+ articles collected

### Daily Brief Workflow
1. Bot creates GitHub Issue with brief
2. You review the content
3. Close issue to approve
4. Bot publishes to GitHub Pages automatically

## 🎯 Expected Results

**First Hour:**
- 0-10 articles found and filtered
- 1 tweet published (if articles found)
- Queue builds up with relevant articles

**First Day:**
- 10-50 articles processed (depending on news volume)
- ~16-24 tweets published (one per hour)
- 1 daily brief generated and published

**Ongoing:**
- Consistent stream of Bitcoin mining news
- Professional, AI-curated content
- Daily comprehensive analysis reports

## 🔧 Troubleshooting

### No Tweets Published?
- Check Twitter API credentials in Secrets
- View Actions logs for errors
- Verify bot_state.json has articles in queue

### No Articles Found?
- EventRegistry API key valid?
- Check logs for "articles marked as relevant"
- Keywords might be too narrow (edit news_processor.py)

### Bot Not Running?
- GitHub Actions enabled?
- Workflows exist in `.github/workflows/`?
- Check Actions tab for error messages

### Daily Brief Not Generated?
- Need at least 5 articles collected
- Check last_brief_date in bot_state.json
- Gemini API key valid and has quota?

## 📚 Next Steps

1. **Read SETUP.md** for detailed configuration options
2. **Review copilot_instructions.md** to understand the codebase
3. **Customize keywords** in news_processor.py for your needs
4. **Adjust AI prompts** in gemini_interface.py for your style
5. **Monitor and iterate** based on published content quality

## 💡 Pro Tips

- **Test locally first**: Run `python test_bot.py` before deploying
- **Start with manual triggers**: Don't rely on schedule until tested
- **Review first tweets**: Check quality before leaving on auto-pilot
- **Monitor API quotas**: Free tiers have limits
- **Backup bot_state.json**: Before making major changes
- **Use workflow_dispatch**: For on-demand testing

## 🆘 Need Help?

1. Check logs in GitHub Actions
2. Review SETUP.md for common issues  
3. Read error messages carefully
4. Open an issue with logs and details

---

**Ready to go!** Your bot should now be running automatically. Check back in an hour to see your first tweets! 🎉
