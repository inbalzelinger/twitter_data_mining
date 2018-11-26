from elasticsearch import Elasticsearch
import requests
import json

class Elastic_search:

    def __init__(self, config_parser):
        self.port = config_parser.elastic_search_config['port']
        self.host = config_parser.elastic_search_config['host']
        self.elastic_url = "http://{0}:{1}".format(self.host, self.port)
        try:
            self.check_elastic_search_availability()
        except:
            print("elasticsearch is not availble ")
        self.elastic = self.__create_elastic_search_object(config_parser)

    def __create_elastic_search_object(self, config_parser):
        return Elasticsearch([{'host': self.host, 'port': self.port}])


    def exp(self):
        r = requests.get('http://localhost:9200')
        i = 1
        while r.status_code == 200:
            r = requests.get('http://swapi.co/api/people/' + str(i))
            self.elastic.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))
            i = i + 1
        print(i)
        print(self.elastic.get(index='sw', doc_type='people', id=5))
        self.elastic.search(index="sw", body={"query": {"match": {'name': 'Darth Vader'}}})


    def check_elastic_search_availability(self):
        ##TODO not sure this will point the problem if there wont be availability. use exit code.
        try:
            requests.get(self.elastic_url)
            print('elastic search is available')
        except:
            print('check_elastic_search_availability problem')



