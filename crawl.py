import tweepy
import time
import json
import re

# Twitter API credentials (replace with your new token)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFlqwAEAAAAAWH64YQtsETF9YsD1RLvhB3FUCrU%3D3QVNRBB9VwYDilyEQ6mz3Q4LsYP4nVqUagz53gJ0NGhOogrHsn"

# Authenticate with Twitter API v2
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# List of Twitter handles to crawl
handles = [
    "elonmusk", "jordanbpeterson", "joerogan", "Malala", 
    "neiltyson", "jk_rowling", "EmmaWatson", "VancityReynolds"
]

def crawl_tweets(handle, count=100):
    tweets = []
    try:
        user = client.get_user(username=handle)
        if user.data:
            user_id = user.data.id
            response = client.get_users_tweets(
                id=user_id,
                max_results=100,
                tweet_fields=['created_at', 'referenced_tweets'],
                expansions=['referenced_tweets.id'],
                exclude=['retweets']
            )
            if response.data:
                for tweet in response.data:
                    if len(tweets) >= count:
                        break
                    if tweet.referenced_tweets and tweet.referenced_tweets[0].type == 'replied_to':
                        original_tweet = next((t for t in response.includes['tweets'] if t.id == tweet.referenced_tweets[0].id), None)
                        if original_tweet:
                            # Filter out short comments and video comments
                            if len(tweet.text) > 35 and not re.search(r'https?://\S+', tweet.text):
                                tweets.append({
                                    'comment': tweet.text,
                                    'original_tweet': original_tweet.text,
                                    'created_at': str(tweet.created_at)
                                })
        print(f"Collected {len(tweets)} comments from @{handle}")
    except tweepy.errors.TweepyException as e:
        print(f"Error collecting tweets from @{handle}: {str(e)}")
    return tweets

# Crawl tweets for each handle
all_tweets = {}
for handle in handles:
    all_tweets[handle] = crawl_tweets(handle)
    time.sleep(1)  # Wait for 10 seconds between each user to avoid rate limiting

# Process or store the collected tweets as needed
for handle, tweets in all_tweets.items():
    print(f"@{handle}: Collected {len(tweets)} comments")
    # Save tweets to a JSON file for each person
    filename = f"{handle}_comments.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=4)
    print(f"Saved comments for @{handle} to {filename}")
