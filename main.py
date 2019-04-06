import tweepy
from elasticsearch import Elasticsearch
from tweepy import OAuthHandler
from tweepy import Stream
import Menu
from ml_algo.kmeans import kmeans_algo
from stream_api import StreamApi
from config_parser import Config_parser
from elasticsearch_dsl import Search
import ArabiziCheck

MAX_RESULTS = 200000
INDEX_NAME = "twitter_index"
DOC_TYPE = "twitter"
TWITTER_TIMEOUT = 1

def main():
    conf_dictionary = read_configuration_file(r'configuration/configuration.conf')
    auth = OAuthHandler(conf_dictionary['consumer_key'], conf_dictionary['consumer_secret'])
    auth.set_access_token(conf_dictionary['access_token'], conf_dictionary['access_token_secret'])
    tweepy.API(auth)
    menu = Menu.menu()
    location = menu.location()
    quary_filters = menu.aggregate_by()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.create(index= INDEX_NAME, ignore=400)
    es.indices.create(index= "arabizi_index", ignore=400)
    listener = StreamApi(es)
    stream = Stream(auth=auth, listener=listener, timeout=TWITTER_TIMEOUT)
    try:
        stream.filter(locations=location)
    except Exception as e:
        print(e)
    createAggregation(quary_filters,es)
    kmeans_algo(es, 6)
    arabiziChecker = ArabiziCheck.arabiziChecker()
    check_arabizi_from_und(es,arabiziChecker)


def createQuery(quary_filters, es, index_name = INDEX_NAME):
    res = es.search(index=index_name, doc_type="twitter", body={"query": {"match": {"content": quary_filters[0]}}})
    print("{} documents found".format(res['hits']['total']))
    for doc in res['hits']['hits']:
        print("{0}) {1}".format(doc['_id'], doc['_source']['content']))


def createAggregation(field, es, index_name = INDEX_NAME):
    ##enable the field (nessecary if its a test field
    es.indices.put_mapping(doc_type=DOC_TYPE, index= INDEX_NAME,
                           body={"properties": {"user.lang": { "type":"text","fielddata": "true"}}})
    s = Search(using=es, index = INDEX_NAME, doc_type=DOC_TYPE)
    s.aggs.bucket('by_lang', 'terms', field=field)
    t = s.execute()
    print(t.aggregations.by_lang.buckets)
    for item in t.aggregations.by_lang.buckets:
        print(item.doc_count)


def check_arabizi_from_und(es,arabiziChecker, language = 'en'):
    sum_of_arabizi = 0
    arabizi_tweets = []
    es.indices.put_settings(index=INDEX_NAME,body={"index": {"max_result_window": MAX_RESULTS}})
    res = es.search(index=INDEX_NAME, doc_type= DOC_TYPE,
                    body={"size":MAX_RESULTS,"query": {"match_all":{}}})
    print("{0} {1} tweets found".format(res['hits']['total'], language))
    i=0
    for tweet in res['hits']['hits']:
        i+=1
        if tweet["_source"] is not None:
            if 'text' in tweet["_source"]:
                if arabiziChecker.checkTweet(tweet["_source"]['text']):
                    arabizi_tweets.append(tweet["_source"]['text'])
                    print("arabizi\n")
                    sum_of_arabizi += 1
    print("sum_of_arabizi = {}".format(sum_of_arabizi))
    with open('configuration\output.txt', 'w', encoding='UTF-8') as output_file:
        for tweet in arabizi_tweets:
            output_file.write(tweet)
        output_file.write("\ntweets number = {}".format(i))


def read_configuration_file(conf_file_path):
    conf_dictionary = {}
    config_parser = Config_parser(conf_file_path)
    conf_dictionary['consumer_key'] = config_parser.twitter_for_developers_config['API_key']
    conf_dictionary['consumer_secret'] = config_parser.twitter_for_developers_config['API_secret_key']
    conf_dictionary['access_token'] = config_parser.twitter_for_developers_config['Access_token']
    conf_dictionary['access_token_secret'] = config_parser.twitter_for_developers_config['Access_token_secret']
    return conf_dictionary

def create_user_locartion_dict(es):
    i = 0
    res = es.search(index=INDEX_NAME, doc_type=DOC_TYPE,
                    body={"size":MAX_RESULTS,"query": {"match_all":{}}})
    for tweet in res['hits']['hits']:
        if 'user.location' in tweet["_source"]:
            i += 1
    print(i)


if __name__ == '__main__':
    main()






