import tweepy
from elasticsearch import Elasticsearch, exceptions
from tweepy import OAuthHandler
from tweepy import Stream
import Menu
from stream_api import StreamApi
from config_parser import Config_parser
from elasticsearch_dsl import Search



def main():
    config_parser = Config_parser(r'configuration\configuration.conf')
    consumer_key = config_parser.twitter_for_developers_config['API_key']
    consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
    access_token = config_parser.twitter_for_developers_config['Access_token']
    access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    tweepy.API(auth)
    menu=Menu.menu()
    location=menu.location()
    quary_filters=menu.aggregate_by()
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.create(index='twitter_index', ignore=400)
    listener = StreamApi(es)
    stream = Stream(auth=auth, listener=listener, timeout=2)
    try:
        stream.filter(locations=location)
    except Exception as e:
        print(e)
    createAggregation(quary_filters,es)



def createQuery(quary_filters, es):
    res = es.search(index='twitter_index', doc_type="twitter", body={"query": {"match": {"content": quary_filters[0]}}})
    print("%d documents found" % res['hits']['total'])
    for doc in res['hits']['hits']:
        print("%s) %s" % (doc['_id'], doc['_source']['content']))

def createAggregation(field,es):
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






