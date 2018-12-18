import tweepy
import json
import requests
from elasticsearch import Elasticsearch

from config_parser import Config_parser
from elastic_search import Elastic_search
from twitter_mining import Twitter


def main():
    print("quastions system\n")
    analysis_kind = input("for sentiment please enter 1\n")
    if analysis_kind == 1:
        name = input("please enter a name\n")
        country = input("please enter the contrys that you want to collect the information from"
                        "at the end please click 1.\n")


    # api = tweepy.API(auth)
    # places = api.geo_search(query="USA", granularity="country")
    # place_id = places[0].id
    #
    # tweets = api.search(q="place:%s" % place_id)
    # for tweet in tweets:
    #     print tweet.text + " | " + tweet.place.name if tweet.place else "Undefined place"


    configuration = Config_parser(r'configuration\configuration.conf')
    twitter_api = Twitter(configuration)
    es = Elastic_search(configuration)
    es.elastic.indices.create(index='twitter_index', ignore=400)







if __name__ == '__main__':
    main()






