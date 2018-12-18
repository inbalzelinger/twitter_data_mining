import tweepy
import json
import requests
from elasticsearch import Elasticsearch
from tweepy import OAuthHandler
from tweepy import Stream

from twitter_stream_listener import twitter_stream_listener

from config_parser import Config_parser
from elastic_search import Elastic_search
from twitter_mining import Twitter
from Menu import menu

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def main():
    key_words=menu.key_words(None)
    quary_filters=menu.query_filters(None)
    #configuration = Config_parser(r'configuration\configuration.conf')
    #twitter_api = Twitter(configuration)
    #es = Elastic_search(configuration)


    listener = twitter_stream_listener(es);
    config_parser = Config_parser(r'configuration.conf')
    consumer_key = config_parser.twitter_for_developers_config['API_key']
    consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
    access_token = config_parser.twitter_for_developers_config['Access_token']
    access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    stream = Stream(auth=auth, listener=listener, timeout=5)
    stream.filter(track=key_words)

    es.indices.create(index='twitter_index', ignore=400)
    createQuery(quary_filters)

def createQuery(quary_filters,index):
    res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"content": quary_filters[0]}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))


if __name__ == '__main__':
    main()






