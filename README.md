# Twitter Scraper

## Setup
```bash
cd ~/Code/twitter\ scrape
```

## Usage
```bash
# Basic search
uv run scrape_twitter.py "from:elonmusk since:2024-01-01"

# Search with limit and CSV output
uv run scrape_twitter.py "ukraine lang:en" --limit 50 --format csv

# Print to console instead of saving
uv run scrape_twitter.py "#python" --limit 10 --print

# Custom output filename
uv run scrape_twitter.py "AI" --limit 100 --output ai_tweets.json
```

## Query Examples
- `from:username` - tweets from specific user
- `to:username` - tweets mentioning user  
- `#hashtag` - tweets with hashtag
- `since:2024-01-01` - tweets after date
- `until:2024-12-31` - tweets before date
- `lang:en` - English tweets only
- `ukraine` - keyword search
