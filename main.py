import tweepy
import json
import requests
from elasticsearch import Elasticsearch

from config_parser import Config_parser
from elastic_search import Elastic_search
from twitter_mining import Twitter


def main():
    configuration = Config_parser(r'configuration\configuration.conf')
    twitter_api = Twitter(configuration)
    es = Elastic_search(configuration)
    es.elastic.indices.create(index='twitter_index', ignore=400)







if __name__ == '__main__':
    main()






