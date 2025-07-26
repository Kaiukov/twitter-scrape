# Twitter Scraper (twscrape)

## Setup
```bash
cd ~/Code/twitter\ scrape

# Install and setup account
uv add twscrape
twscrape add_account username email@example.com password
twscrape login_accounts
```

## Usage
```bash
uv run scrape_twitter.py "from:elonmusk since:2024-01-01"
uv run scrape_twitter.py "ukraine lang:en" --limit 50 --format csv
uv run scrape_twitter.py "AI" --limit 10 --print
```

## Notes
- Requires Twitter account credentials
- Async-based for better performance
- Handles authentication automatically
