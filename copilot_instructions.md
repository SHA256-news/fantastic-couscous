# GitHub Copilot Instructions - SHA256 News Bot

## Project Context

You are working on the SHA256 News Bitcoin Mining News Aggregator Bot - an automated system that:
1. Fetches Bitcoin mining articles from EventRegistry
2. Uses Google Gemini AI to filter for relevance
3. Generates engaging tweet content with AI
4. Publishes to Twitter with appropriate images
5. Creates daily comprehensive briefs
6. Maintains a GitHub Pages website

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints where helpful
- Prefer explicit over implicit
- Use descriptive variable names
- Keep functions focused and single-purpose

### Logging
- Use logging module, not print()
- Log levels: INFO for progress, WARNING for recoverable issues, ERROR for failures
- Include context in log messages
- Log before and after important operations

### Error Handling
- Use try-except blocks for external API calls
- Fail gracefully, don't crash the bot
- Return sensible defaults on errors
- Log errors with traceback when appropriate

### Documentation
- Docstrings for all public functions
- Explain non-obvious logic with comments
- Keep README up to date
- Document configuration options

## Module-Specific Guidelines

### gemini_interface.py
When working on AI interactions:
- Always handle response structure variations
- Truncate inputs to stay within model limits
- Provide clear, specific prompts
- Parse responses robustly
- Return None on failures, not exceptions

### news_processor.py
When handling article processing:
- Use ordered CSS selectors for content extraction
- Filter out short/boilerplate text
- Handle network errors gracefully
- Deduplicate using both URL and event URI
- Maintain global state correctly

### twitter_publisher.py
When implementing Twitter features:
- Use v2 API for tweets, v1.1 for media
- Handle rate limits
- Construct proper permalinks
- Store metadata for website
- Reply with source URL separately

### image_manager.py
When managing images:
- Check IMAGE_LIBRARY_ACTIVE flag first
- Match case-insensitively for company names
- Provide random selection for conceptual images
- Handle missing files gracefully
- Create placeholders when needed

### github_manager.py
When updating GitHub:
- Use PyGithub library
- Handle file existence checks
- Update if exists, create if not
- Commit with descriptive messages
- Handle authentication errors

### daily_brief_generator.py
When generating briefs:
- Use markdown for source format
- Convert to styled HTML
- Generate metadata with AI
- Keep consistent formatting
- Include proper navigation

## Testing Guidelines

### Before Committing
- Test module independently if possible
- Check imports work correctly
- Verify environment variables load
- Ensure backwards compatibility
- Run on sample data

### Integration Testing
- Test full bot cycle locally
- Verify state persistence
- Check GitHub updates work
- Confirm Twitter posting (use test account)
- Validate website updates

## Configuration Best Practices

### Environment Variables
- Never hardcode secrets
- Use .env for local development
- Document all variables in .env.example
- Set GitHub Secrets for production
- Provide sensible defaults where possible

### File Paths
- Use os.path.join() for path construction
- Use absolute paths in production
- Handle missing directories gracefully
- Create directories as needed
- Don't assume current directory

## AI/LLM Integration Best Practices

### Prompt Engineering
- Be specific about output format
- Provide clear examples
- Set constraints explicitly
- Ask for structured responses
- Include error cases in instructions

### Response Handling
- Parse JSON carefully
- Check for expected keys
- Handle partial responses
- Validate output format
- Provide fallbacks

## State Management

### Global State
- Initialize from loaded state
- Update consistently
- Save after critical operations
- Persist to GitHub for durability
- Clear appropriately (e.g., daily URLs)

### Queue Management
- LIFO (most recent first)
- Deduplicate before adding
- Remove after successful processing
- Re-add on retryable failures
- Limit queue size if needed

## GitHub Actions Considerations

### Workflow Design
- Use appropriate triggers (schedule, manual)
- Set timeouts appropriately
- Upload logs as artifacts
- Use latest action versions
- Cache dependencies when beneficial

### Secrets Management
- Never log secret values
- Use secrets for all credentials
- Set secrets at repository level
- Document required secrets in README
- Rotate periodically

## Common Patterns

### API Call Pattern
```python
try:
    response = api_call()
    if response and response.is_valid:
        return process(response)
    logging.warning("Invalid response")
    return default_value
except Exception as e:
    logging.error(f"API call failed: {e}")
    return default_value
```

### State Update Pattern
```python
# Do operation
result = perform_operation()

if result.success:
    # Update global state
    PROCESSED_ITEMS.add(result.item_id)
    
    # Save state
    save_bot_state_to_file()
    
    # Persist to GitHub
    github_manager.push_state_to_github(REPO_NAME)
```

### Content Processing Pattern
```python
# Fetch
content = fetch_content(url)

# Validate
if not validate(content):
    logging.warning("Invalid content")
    return None

# Process with AI
result = ai_process(content)

# Verify output
if not verify(result):
    logging.error("AI processing failed")
    return fallback_value

return result
```

## Debugging Tips

### Local Debugging
- Set logging to DEBUG level
- Print state variables
- Use breakpoints in IDE
- Test with minimal inputs
- Check .env is loaded

### Production Debugging
- Check GitHub Actions logs
- Download bot.log artifact
- Verify secrets are set
- Check API rate limits
- Review state file

## Performance Considerations

### API Usage
- Minimize API calls where possible
- Cache results when appropriate
- Batch operations
- Respect rate limits
- Use async if beneficial

### Content Processing
- Truncate large inputs
- Use efficient parsers (lxml)
- Limit queue size
- Clean up old state
- Archive historical data

## Security Considerations

### Secrets
- Never commit .env
- Use GitHub Secrets
- Rotate credentials regularly
- Minimize secret scope
- Audit access logs

### Input Validation
- Sanitize URLs
- Validate JSON structure
- Check file paths
- Limit input sizes
- Escape HTML when needed

## Extension Guidelines

### Adding New Features
1. Document in README
2. Add configuration options
3. Update .env.example
4. Handle backwards compatibility
5. Test thoroughly
6. Update documentation

### Adding New APIs
1. Create separate module
2. Handle authentication
3. Implement error handling
4. Add to requirements.txt
5. Document in MCP
6. Test integration

## Code Review Checklist

- [ ] Follows project style
- [ ] Has proper error handling
- [ ] Includes logging
- [ ] Updates documentation
- [ ] No hardcoded secrets
- [ ] Backwards compatible
- [ ] Tested locally
- [ ] GitHub Actions pass

## Quick Reference

### Running Locally
```bash
# Main bot
python -m bitcoin_miner_bot.main

# Daily brief
python -m bitcoin_miner_bot.daily_brief_script
```

### Common Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Check syntax
python -m py_compile bitcoin_miner_bot/main.py

# Run tests (if added)
python -m pytest

# Check logs
tail -f bot.log
```

### File Locations
- Source code: `bitcoin_miner_bot/`
- Config: `.env`, `.env.example`
- State: `bot_state.json`
- Logs: `bot.log`
- Images: `images/`
- Website: `gh-pages/`
- Workflows: `.github/workflows/`

---

These instructions help maintain consistency and quality across the SHA256 News bot codebase.