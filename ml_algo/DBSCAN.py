import numpy as np



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
def cluster(coordinates_array):
    clusters_dict={}
    clustering = DBSCAN(eps=3, min_samples=2).fit(coordinates_array)
    labels=clustering.labels_
    print(type(labels))
    for i in labels.length():
        if labels[i] not in clusters_dict.keys():
            clusters_dict[labels[i]] = []
        clusters_dict[labels[i]].append(coordinates_array[i])
    print(clusters_dict)
"""







