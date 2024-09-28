import tweepy
import time
import json

# Twitter API credentials (replace with your new token)
bearer_token = "AAAAAAAAAAAAAAAAAAAAAFlqwAEAAAAAWH64YQtsETF9YsD1RLvhB3FUCrU%3D3QVNRBB9VwYDilyEQ6mz3Q4LsYP4nVqUagz53gJ0NGhOogrHsn"

# Authenticate with Twitter API v2
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# List of Twitter handles to crawl
handles = [
    "elonmusk", "jordanbpeterson", "joerogan",
    "BernieSanders", "narendramodi", "Malala", "StephenKing",
    "neiltyson", "VP"
]

def crawl_tweets(handle, count=50):
    tweets = []
    try:
        user = client.get_user(username=handle)
        if user.data:
            user_id = user.data.id
            response = client.get_users_tweets(
                id=user_id,
                max_results=100,
                tweet_fields=['created_at'],
                exclude=['retweets', 'replies']
            )
            if response.data:
                for tweet in response.data:
                    if len(tweets) >= count:
                        break
                    tweets.append(tweet)
        print(f"Collected {len(tweets)} non-repost tweets from @{handle}")
    except tweepy.errors.TweepyException as e:
        print(f"Error collecting tweets from @{handle}: {str(e)}")
    return tweets

# Crawl tweets for each handle
all_tweets = {}
for handle in handles:
    all_tweets[handle] = crawl_tweets(handle)
    time.sleep(10)  # Wait for 60 seconds between each user to avoid rate limiting

# Process or store the collected tweets as needed
for handle, tweets in all_tweets.items():
    print(f"@{handle}: Collected {len(tweets)} non-repost tweets")
    # Save tweets to a JSON file for each person
    filename = f"{handle}_tweets.json"
    tweet_data = [{"text": tweet.text, "created_at": str(tweet.created_at)} for tweet in tweets]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(tweet_data, f, ensure_ascii=False, indent=4)
    print(f"Saved tweets for @{handle} to {filename}")
