from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import os
from tweepy import Stream


class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status_code):
        print(status_code)


def tweet_stream():
    listener = StdOutListener()
    auth = OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    stream = Stream(auth, listener)

    stream.filter(track=['enchente','alagado','agua'])


tweet_stream()