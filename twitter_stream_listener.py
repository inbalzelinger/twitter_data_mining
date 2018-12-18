from textwrap import TextWrapper
import tweepy
import json


class twitter_stream_listener(tweepy.StreamListener):

    def __init__(self,es):
        status_wrapper = TextWrapper(width=60, initial_indent='     ', subsequent_indent='      ')
        self.es = es

    def on_status(self, status):
        print("{} {}".format(status.author.screen_name, status.created_at))
        json_data = status._json
        print(json_data['text'])
        self.es.index(index="twitter_index",
                 doc_type="twitter",
                 body=json_data,
                 ignore=400)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False



