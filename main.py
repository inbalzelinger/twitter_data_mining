import tweepy
import json
import requests
from elasticsearch import Elasticsearch

from config_parser import Config_parser
from twitter_mining import Twitter


def main():
    configuration = Config_parser()
    twitter = Twitter(configuration)
    tweets = twitter.read_tweets("realDonaldTrump", 3)
    for tweet in tweets:
        print(tweet.text)



if __name__ == '__main__':
    main()



# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
# r = requests.get('http://localhost:9200')
# i = 1
# while r.status_code == 200:
#     r = requests.get('http://swapi.co/api/people/' + str(i))
#     es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
#     i = i + 1
#
# print(i)
# print(es.get(index='sw', doc_type='people', id=5))



