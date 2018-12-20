import tweepy
import sys

from elasticsearch_dsl import A
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime
from config_parser import Config_parser
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import aggs
from Menu import menu
import ArabiziCheck

config_parser = Config_parser(r'configuration.conf')
consumer_key = config_parser.twitter_for_developers_config['API_key']
consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
access_token = config_parser.twitter_for_developers_config['Access_token']
access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
places = api.geo_search(query="USA", granularity="country")
place_id = places[0].id

"""
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

es.indices.create(index='twitter_index', ignore=400)

class Streamapi(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='     ', subsequent_indent='      ')

    def on_status(self, status):
        print("{} {}".format(status.author.screen_name, status.created_at))
        json_data = status._json
        #print(json_data['text'])
        es.index(index = "twitter_index",
                              doc_type = "twitter",
                              body= json_data,
                              ignore = 400)


stremer = tweepy.Stream(auth=auth, listener=Streamapi(), timeout=5)
#key_words = menu.key_words(None)
#query_filters=menu.query_filters(None)
#stremer.filter(None,key_words)



#res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"user.location": 'usa'}}})
#res = es.search(index="twitter_index", body={"query": {"match_all": {}}})
#print("%d tweets found" % res['hits']['total'])

#for doc in res['hits']['hits']:
 #   print("%s) %s" % (doc['_id'], doc['_source']['content']))

#s = Search()
#a = A('terms', field='user.location')
#s.aggs.bucket('category_terms', a)

s = Search(using=es, index="twitter_index", doc_type="twitter")
#s.aggs.bucket('by_location', 'terms', field='user.location')
s.aggs.bucket('by_lang', 'terms', field='lang')
t=s.execute()


print(t.aggregations.by_location.buckets)
for item in t.aggregations.by_location.buckets:
    print(item.doc_count)


print(t.aggregations.by_lang.buckets)
for item in t.aggregations.by_lang.buckets:
    print(item.doc_count)

res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"lang": 'und'}}})
print("%d tweets found" % res['hits']['total'])

for doc in res['hits']['hits']:
   print(doc)
   """
arabiziChecker=ArabiziCheck.arabiziChecker()
if arabiziChecker.checkTweet("la2 la2 la2 la2 la2 la2 la2!! la2"):
    print("arabiz\n")
print("not arabizi\n")
