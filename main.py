import tweepy
import json
import requests
from elasticsearch import Elasticsearch
from tweepy import OAuthHandler
from tweepy import Stream

import Menu
from twitter_stream_listener import twitter_stream_listener
from config_parser import Config_parser
from elastic_search import Elastic_search
from twitter_mining import Twitter
from Menu import menu
from elasticsearch_dsl import Search

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
config_parser = Config_parser(r'configuration.conf')
consumer_key = config_parser.twitter_for_developers_config['API_key']
consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
access_token = config_parser.twitter_for_developers_config['Access_token']
access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']

def main():
    menu=Menu.menu()
    #key_words=menu.key_words()
    location=menu.location()
    quary_filters=menu.aggregate_by()

    #create stream listener
    listener = twitter_stream_listener(es)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    stream = Stream(auth=auth, listener=listener, timeout=5)
    stream.filter(locations=location)
    createQuery(quary_filters,index)



def createQuery(quary_filters,index):
    res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"content": quary_filters[0]}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))

def createAggregation(field,index):
    s = Search(using=es, index="twitter_index", doc_type="twitter")
    s.aggs.bucket('by_lang', 'terms', field=field)
    t = s.execute()

    print(t.aggregations.by_lang.buckets)
    for item in t.aggregations.by_lang.buckets:
        print(item.doc_count)

    res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"lang": 'und'}}})
    print("%d tweets found" % res['hits']['total'])

    for doc in res['hits']['hits']:
        print(doc)

if __name__ == '__main__':
    main()






