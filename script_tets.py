import tweepy
from tweepy import OAuthHandler
from textwrap import TextWrapper
from datetime import datetime
from config_parser import Config_parser
from elasticsearch import Elasticsearch

config_parser = Config_parser(r'configuration\configuration.conf')
consumer_key = config_parser.twitter_for_developers_config['API_key']
consumer_secret = config_parser.twitter_for_developers_config['API_secret_key']
access_token = config_parser.twitter_for_developers_config['Access_token']
access_token_secret = config_parser.twitter_for_developers_config['Access_token_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
places = api.geo_search(query="USA", granularity="country")
place_id = places[0].id


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
es.indices.create(index='twitter_index', ignore = 400)
es.indices.create(index='test-index', ignore = 400)

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])



class Streamapi(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent='     ', subsequent_indent='      ')

    def on_status(self, status):


        print("{} {}".format(status.author.screen_name, status.created_at))
        json_data = status._json
        print(json_data)
        print(json_data['text'])
        es.index(index = "twitter_index",
                              doc_type = "twitter",
                              body= json_data,
                              ignore = 400
                 )

stremer = tweepy.Stream(auth=auth, listener=Streamapi(), timeout=5)
#terms = ['prince', '#trump']
stremer.filter(locations=[24.70007, 22.0, 36.86623, 31.58568])





