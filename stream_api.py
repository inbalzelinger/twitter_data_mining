from textwrap import TextWrapper
import tweepy
from elasticsearch import Elasticsearch
from tweepy import OAuthHandler
from config_parser import Config_parser

config_parser = Config_parser(r'configuration\configuration.conf')
consumer_key = config_parser.twitter_for_developers_config['API_key']
consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
access_token = config_parser.twitter_for_developers_config['Access_token']
access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
tweepy.API(auth)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='twitter_index', ignore=400)


class StreamApi(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='     ', subsequent_indent='      ')

    def __init__(self, es):
        tweepy.StreamListener.__init__(self)
        self.es = es


    def on_status(self, status):
        print("{} {}".format(status.author.screen_name, status.created_at))
        json_data = status._json
        print(json_data['text'])
        es.index(index="hadar2",
                 doc_type="twitter",
                 body=json_data,
                 ignore=400)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
