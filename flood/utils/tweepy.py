from tweepy import OAuthHandler, API, error, Cursor
import os
from datetime import timedelta
from flood.endpoints import endpoints_exception


def to_dict(tweet):
    dt = tweet.created_at - timedelta(hours=3)
    result = {
        "tweet_user_name": tweet.user.name,
        "tweet_user_screen_name": tweet.user.screen_name,
        "tweet_text": tweet.full_text,
        "tweet_url": "https://twitter.com/{0}/status/{1}".format(tweet.user.screen_name, tweet.id),
        "favorite_count": tweet.favorite_count,
        "retweet_count": tweet.retweet_count,
        "created_at": dt.strftime("%a ,%d-%m-%Y %H:%M:%S")
    }
    return result


def authenticate_twitter_app():
    auth = OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
    return API(auth)


def get_user_timeline_tweets(num_tweets, user):
    tweets = []
    try:
        for tweet in Cursor(authenticate_twitter_app().user_timeline, id=user, tweet_mode='extended').items(num_tweets):
            tweets.append(to_dict(tweet))
        return tweets
    except error.RateLimitError:
        raise endpoints_exception(429, "NUMBER OF REQUESTS PER HOUR HAS BEEN EXCEEDED")
    except error.TweepError:
        raise endpoints_exception(500, "APPLICATION FAILED TO MAINTAIN CONNECTION WITH TWITTER")