import tweepy
import sys
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime
from config_parser import Config_parser
from elasticsearch import Elasticsearch

config_parser = Config_parser(r'configuration\configuration.conf')
consumer_key = config_parser.twitter_for_developers_config['API_key']
consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
access_token = config_parser.twitter_for_developers_config['Access_token']
access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='twitter_index', ignore = 400)

class Streamapi(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='     ', subsequent_indent='      ')

    def on_status(self, status):
        print("{} {}".format(status.author.screen_name, status.created_at))
        json_data = status._json
        print(json_data['text'])
        es.index(index = "twitter_index",
                              doc_type = "twitter",
                              body= json_data,
                              ignore = 400)


stremer = tweepy.Stream(auth=auth, listener=Streamapi(), timeout=5)
terms = ['prince', '#trump']
stremer.filter(None,terms)

