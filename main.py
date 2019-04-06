import tweepy
from elasticsearch import Elasticsearch, exceptions
from tweepy import OAuthHandler
from tweepy import Stream
import Menu
from kmeans import kmeans_algo
from stream_api import StreamApi
from config_parser import Config_parser
from elasticsearch_dsl import Search
import ArabiziCheck



def main():
    conf_dictionary = read_configuration_file('configuration.conf')
    auth = OAuthHandler(conf_dictionary['consumer_key'], conf_dictionary['consumer_secret'])
    auth.set_access_token(conf_dictionary['access_token'], conf_dictionary['access_token_secret'])
    tweepy.API(auth)
    menu = Menu.menu()
    location = menu.location()
    quary_filters = menu.aggregate_by()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.create(index='twitter_index', ignore=400)
    # kmeans_algo(es, 7, location)
    listener = StreamApi(es)
    stream = Stream(auth=auth, listener=listener, timeout=1)
    try:
        stream.filter(locations=location)
    except Exception as e:
        print(e)
    createAggregation(quary_filters,es)
    #create_user_locartion_dict(es)
    arabiziChecker = ArabiziCheck.arabiziChecker()
    check_arabizi_from_und(es,arabiziChecker)


def createQuery(quary_filters, es, index_name = 'twitter_index'):
    res = es.search(index=index_name, doc_type="twitter", body={"query": {"match": {"content": quary_filters[0]}}})
    print("{} documents found".format(res['hits']['total']))
    for doc in res['hits']['hits']:
        print("{0}) {1}".format(doc['_id'], doc['_source']['content']))


def createAggregation(field,es, index_name = 'twitter_index'):
    ##TODO enable the field first.
    #es.put_mapping(doc_type='twitter_index', body='properties: {lang: {type: text,fielddata: true}}')
    s = Search(using=es, index = index_name, doc_type="twitter")
    s.aggs.bucket('by_lang', 'terms', field=field)
    t = s.execute()
    print(t.aggregations.by_lang.buckets)
    for item in t.aggregations.by_lang.buckets:
        print(item.doc_count)


def check_arabizi_from_und(es,arabiziChecker, language = 'en'):
    sum_of_arabizi = 0
    arabizi_tweets = []
    res = es.search(index='twitter_index', doc_type="twitter", body={"size":'10000',"query": {"match_all":{}}})
    #res = es.search(index='twitter_index', doc_type="twitter", body={"size":'10000',"query": {"match": {"in_reply_to_user_id_str": 1055932978113724416}}})
    print("{0} {1} tweets found".format(res['hits']['total'], language))
    i=0
    for tweet in res['hits']['hits']:
        i+=1
        if tweet["_source"] is not None:
            #print("{}(text)s".format(tweet["_source"]))
            if 'text' in tweet["_source"]:
                if arabiziChecker.checkTweet(tweet["_source"]['text']):
                    arabizi_tweets.append(tweet["_source"]['text'])
                    print("arabizi\n")
                    sum_of_arabizi += 1
    print("sum_of_arabizi = {}".format(sum_of_arabizi))
    print("the arabizi tweets are: {}".format(arabizi_tweets))
        #print("not arabizi\n")
    print("tweets number = {}".format(i))


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
    res = es.search(index='twitter_index', doc_type="twitter", body={"size":'45000',"query": {"match_all":{}}})
    for tweet in res['hits']['hits']:
        if 'user.location' in tweet["_source"]:
            i += 1
    print(i)

if __name__ == '__main__':
    main()






