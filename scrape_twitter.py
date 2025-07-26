#!/usr/bin/env python3
"""
Twitter Scraper using twscrape
Installation: uv add twscrape
Usage: python scrape_twitter.py "from:elonmusk since:2024-01-01"
"""

import argparse
import json
import csv
import sys
import asyncio
from datetime import datetime
from pathlib import Path

try:
    from twscrape import API, gather
    from twscrape.logger import set_log_level
except ImportError:
    print("❌ twscrape not installed. Install with: uv add twscrape")
    sys.exit(1)


async def scrape_tweets(query, limit=100):
    """Scrape tweets using twscrape"""
    tweets = []
    
    print(f"🔍 Searching for: {query}")
    print(f"📊 Limit: {limit} tweets")
    
    # Suppress verbose logging
    set_log_level("WARNING")
    
    try:
        api = API()  # Initialize API
        
        # Check if accounts are logged in
        accounts = await api.pool.accounts_info()
        if not accounts:
            print("⚠️  No Twitter accounts configured")
            print("💡 Add account with: twscrape add_account username email password")
            return []
        
        # Search tweets
        async for tweet in api.search(query, limit=limit):
            tweet_data = {
                'id': tweet.id,
                'date': tweet.date.isoformat(),
                'content': tweet.rawContent,
                'username': tweet.user.username,
                'displayname': tweet.user.displayname,
                'url': tweet.url,
                'retweet_count': tweet.retweetCount,
                'like_count': tweet.likeCount,
                'reply_count': tweet.replyCount,
                'quote_count': tweet.quoteCount,
                'hashtags': [tag.lower() for tag in tweet.hashtags] if tweet.hashtags else [],
                'mentions': [mention.username for mention in tweet.mentionedUsers] if tweet.mentionedUsers else []
            }
            tweets.append(tweet_data)
            
            # Progress indicator
            if len(tweets) % 10 == 0:
                print(f"📥 Scraped {len(tweets)} tweets...")
    
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        if "No accounts available" in str(e):
            print("💡 Setup: twscrape add_account username email password")
        return []
    
    print(f"✅ Successfully scraped {len(tweets)} tweets")
    return tweets


def save_tweets(tweets, output_format, filename=None):
    """Save tweets to file"""
    if not tweets:
        print("⚠️ No tweets to save")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_format.lower() == "json":
        filename = filename or f"tweets_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(tweets)} tweets to {filename}")
    
    elif output_format.lower() == "csv":
        filename = filename or f"tweets_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if tweets:
                writer = csv.DictWriter(f, fieldnames=tweets[0].keys())
                writer.writeheader()
                for tweet in tweets:
                    # Convert lists to strings for CSV
                    tweet_copy = tweet.copy()
                    tweet_copy['hashtags'] = ', '.join(tweet['hashtags'])
                    tweet_copy['mentions'] = ', '.join(tweet['mentions'])
                    writer.writerow(tweet_copy)
        print(f"💾 Saved {len(tweets)} tweets to {filename}")


async def main():
    parser = argparse.ArgumentParser(
        description="Scrape Twitter using twscrape",
        epilog="""
Setup (first time):
  twscrape add_account username1 email1@example.com password1
  twscrape login_accounts

Examples:
  uv run scrape_twitter.py "from:elonmusk since:2024-01-01"
  uv run scrape_twitter.py "ukraine lang:en" --limit 50 --format csv
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("query", help="Twitter search query")
    parser.add_argument("--limit", "-l", type=int, default=100, 
                       help="Maximum number of tweets (default: 100)")
    parser.add_argument("--format", "-f", choices=["json", "csv"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--print", "-p", action="store_true", 
                       help="Print tweets to console")
    
    args = parser.parse_args()
    
    # Scrape tweets
    tweets = await scrape_tweets(args.query, args.limit)
    
    if not tweets:
        print("❌ No tweets found")
        return
    
    # Output results
    if args.print:
        for tweet in tweets:
            print(f"\n📝 @{tweet['username']} ({tweet['date']})")
            print(f"   {tweet['content']}")
            print(f"   👍 {tweet['like_count']} | 🔄 {tweet['retweet_count']} | 💬 {tweet['reply_count']}")
            print(f"   🔗 {tweet['url']}")
    else:
        save_tweets(tweets, args.format, args.output)


if __name__ == "__main__":
    asyncio.run(main())
