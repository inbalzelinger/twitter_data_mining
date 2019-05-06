import zlib, sys

MAX_RESULTS = 200000
INDEX_NAME = "hadar2"
DOC_TYPE = "twitter"

"""
compress tweets that has coordinates value
 and return their compressed sizes in a dictionary:
 tweet_id: size
"""
def compressTweetsWithCoordinates(es):
    es.indices.put_settings(index=INDEX_NAME, body={"index": {"max_result_window": MAX_RESULTS}})
    res = es.search(index=INDEX_NAME, doc_type=DOC_TYPE,
                    body={"size": MAX_RESULTS, "query": {"match_all": {}}})
    coordinates_compressed={}
    for tweet in res['hits']['hits']:
        if 'coordinates' in tweet["_source"]:
           if tweet["_source"]['coordinates'] is not None:
                if tweet["_source"] is not None:
                    if 'text' in tweet["_source"]:
                        text=tweet["_source"]['text']
                        #print("original size: ",sys.getsizeof(text))
                        compressed=zlib.compress(bytes(text, 'utf-8'),6)
                        coordinates_compressed[tweet["_source"]["id_str"]]=sys.getsizeof(compressed)
                        #print("size after compression: ",sys.getsizeof(compressed))
    print(coordinates_compressed)
    print(len(coordinates_compressed.keys()))
    return coordinates_compressed

def noCoordinatesClustering(es,DBScan_clusters_dict):
    new_clusters_dict=DBScan_clusters_dict.copy()
    es.indices.put_settings(index=INDEX_NAME, body={"index": {"max_result_window": MAX_RESULTS}})
    res = es.search(index=INDEX_NAME, doc_type=DOC_TYPE,
                    body={"size": MAX_RESULTS, "query": {"match_all": {}}})
    for tweet in res['hits']['hits']:
        if tweet["_source"] is not None:
            if 'coordinates' in tweet["_source"]:
                #iterate all tweets in index that has no coordinates
                if tweet["_source"]['coordinates'] is None:
                    if 'text' in tweet["_source"]:
                        text = tweet["_source"]['text']
                        matchCluster=-2
                        min=sys.maxsize
                        #for each cluster (consist of tweets with coordinates):
                        for label in DBScan_clusters_dict.keys():
                            #print("label is: ",label)
                            sumCompressDistance=0
                            for id in DBScan_clusters_dict[label]:
                                r=es.search(index=INDEX_NAME, doc_type=DOC_TYPE,
                                            body={"size": MAX_RESULTS, "query": {"match": {'id_str': id}}})
                                for t in r['hits']['hits']:
                                    coor_text=t["_source"]['text']
                                    compressed_original=zlib.compress(bytes(coor_text, 'utf-8'), 6)
                                    concatinateTweets=coor_text+text
                                    compressed_Concat = zlib.compress(bytes(concatinateTweets, 'utf-8'), 6)
                                    #print("size after compression: ", sys.getsizeof(compressed_original))
                                    sumCompressDistance+=(sys.getsizeof(compressed_Concat)-sys.getsizeof(compressed_original))
                            avgCompressDist=sumCompressDistance/len(DBScan_clusters_dict[label])
                            if avgCompressDist<min:
                                min=avgCompressDist
                                matchCluster=label
                        new_clusters_dict[matchCluster].append(tweet["_source"]["id_str"])
    print(new_clusters_dict)
    return new_clusters_dict