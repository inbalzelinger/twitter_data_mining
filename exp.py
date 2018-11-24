import tweepy
import json
import requests
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')
i = 1
while r.status_code == 200:
    r = requests.get('http://swapi.co/api/people/' + str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
    i = i + 1

print(i)
print(es.get(index='sw', doc_type='people', id=5))



# consumer_key = "XXXXXXXXXXXXXXXXXXXXX"
# consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"
# access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXx"
# access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# api = tweepy.API(auth)
# name = "realDonaldTrump"
# # Number of tweets to pull
# tweetCount = 1
#
# results = api.user_timeline(id=name, count=tweetCount)
#
# for tweet in results:
#    print (tweet.text)