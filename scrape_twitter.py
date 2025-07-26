#!/usr/bin/env python3
"""
Twitter Scraper using snscrape
Installation: uv add snscrape
Usage: python scrape_twitter.py "from:elonmusk since:2024-01-01"
"""

import argparse
import json
import csv
import sys
import ssl
import urllib3
from datetime import datetime
from pathlib import Path

# Disable SSL warnings and configure SSL context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

try:
    import snscrape.modules.twitter as sntwitter
except ImportError:
    print("❌ snscrape not installed. Install with: uv add snscrape")
    sys.exit(1)


def scrape_tweets(query, limit=100, output_format="json"):
    """Scrape tweets based on query and return results"""
    tweets = []
    
    print(f"🔍 Searching for: {query}")
    print(f"📊 Limit: {limit} tweets")
    
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
                
            tweet_data = {
                'id': tweet.id,
                'date': tweet.date.isoformat(),
                'content': tweet.content,
                'username': tweet.user.username,
                'displayname': tweet.user.displayname,
                'url': tweet.url,
                'retweet_count': tweet.retweetCount,
                'like_count': tweet.likeCount,
                'reply_count': tweet.replyCount,
                'quote_count': tweet.quoteCount,
                'hashtags': [tag for tag in tweet.hashtags] if tweet.hashtags else [],
                'mentions': [mention.username for mention in tweet.mentionedUsers] if tweet.mentionedUsers else []
            }
            tweets.append(tweet_data)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"📥 Scraped {i + 1} tweets...")
    
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return []
    
    print(f"✅ Successfully scraped {len(tweets)} tweets")
    return tweets


def save_tweets(tweets, output_format, filename=None):
    """Save tweets to file in specified format"""
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
    
    else:
        print(f"❌ Unsupported format: {output_format}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Twitter using snscrape",
        epilog="""
Examples:
  python scrape_twitter.py "from:elonmusk since:2024-01-01"
  python scrape_twitter.py "ukraine lang:en" --limit 50 --format csv
  python scrape_twitter.py "#python" --limit 200 --output my_tweets.json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("query", help="Twitter search query")
    parser.add_argument("--limit", "-l", type=int, default=100, 
                       help="Maximum number of tweets to scrape (default: 100)")
    parser.add_argument("--format", "-f", choices=["json", "csv"], default="json",
                       help="Output format (default: json)")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--print", "-p", action="store_true", 
                       help="Print tweets to console instead of saving")
    
    args = parser.parse_args()
    
    # Scrape tweets
    tweets = scrape_tweets(args.query, args.limit, args.format)
    
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
    main()
