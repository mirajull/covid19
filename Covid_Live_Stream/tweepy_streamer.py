# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import json

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, fetched_texts_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename, fetched_texts_filename)
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename, fetched_texts_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.fetched_texts_filename = fetched_texts_filename


    def on_data(self, data):
        try:
            #print(data)
            json_load = json.loads(data)
            text = {'text': json_load['text']}
            print(text)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            with open(self.fetched_texts_filename, 'a') as tf:
                tf.write(json.dumps(text))
                tf.write("\n")
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True


    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # Authenticate using config.py and connect to Twitter Streaming API.
    #hash_tag_list = ["corona", "covid19", "corona virus", "covid", "covid 19", "covid 2019"]
    hash_tag_list = ["contact tracing", "contact tracking", "corona privacy",
    "corona application", "covid application", "covid19 application",
    "corona application", "covid application", "covid19 application"]

    fetched_tweets_filename = "live_tweets.txt"
    fetched_texts_filename = "live_texts.txt"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, fetched_texts_filename, hash_tag_list)
