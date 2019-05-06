import numpy as np
from sklearn.cluster import DBSCAN

MAX_RESULTS = 200000
INDEX_NAME = "hadar"
DOC_TYPE = "twitter"
"""
def create_points_dict(es):
    coordinate_dict = {}
    coordinates_array = np.array([])
    i = 0
    res = es.search(index='twitter_index', doc_type="twitter", body={"size":'10000',"query": {"match_all":{}}})
    for tweet in res['hits']['hits']:
        if tweet["_source"] is not None:
            if 'coordinates' in tweet["_source"]:
                if tweet["_source"]['coordinates'] is not None:
                    i += 1
                    print(tweet["_source"]['coordinates'])
                    coordinate_dict[tweet["_source"]["id_str"]] = tweet["_source"]['coordinates']
                    coordinates_array = np.append(coordinates_array, [tweet["_source"]['coordinates']])

    #print(i)
    #print(coordinate_dict)
    #print(coordinates_array)
    return coordinates_array

"""

def create_points_dict(es):
    coordinate_dict = {}
    i = 0
    es.indices.put_settings(index=INDEX_NAME,body={"index": {"max_result_window": MAX_RESULTS}})
    res = es.search(index=INDEX_NAME, doc_type=DOC_TYPE,
                    body={"size":MAX_RESULTS,"query": {"match_all":{}}})
    for tweet in res['hits']['hits']:
        if tweet["_source"] is not None:
            if 'coordinates' in tweet["_source"]:
                if tweet["_source"]['coordinates'] is not None:
                    i += 1
                    coordinate_dict[tweet["_source"]["id_str"]] = tweet["_source"]['coordinates']
    list_of_points = []
    for key, val in coordinate_dict.items():
        list_of_points.append(val['coordinates'])
    point_arr = np.array([])
    print(len(point_arr))
    for point in list_of_points:
        point_arr = np.append(point_arr, point)
    A = np.array([[e[0], e[1]] for e in list_of_points])
    return A,coordinate_dict

"""
run DBSCAN algorithm and clusters the tweets according to coordinates
return dict:
cluster label: list of all tweets id_string that are in the cluster
"""
def cluster(coordinates_array,coordinate_dict):
    clusters_dict={}
    clustering = DBSCAN(eps=3, min_samples=2).fit(coordinates_array)
    labels=clustering.labels_
    print(type(labels))
    print(labels)
    for i in range(labels.shape[0]):
        if labels[i] not in clusters_dict.keys():
            clusters_dict[labels[i]] = []
        #clusters_dict[labels[i]].append(coordinates_array[i])
        clusters_dict[labels[i]].append(list(coordinate_dict.keys())[i])
    print(clusters_dict)
    print(clusters_dict.keys())
    return clusters_dict








