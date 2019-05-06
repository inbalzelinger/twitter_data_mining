#“coordinates” attributes is formatted as [LONGITUDE, latitude],
#“geo” attribute is formatted as [latitude, LONGITUDE].

import seaborn as sns;
from sklearn.cluster import KMeans

sns.set()  # for plot styling


import numpy as np

MAX_RESULTS = 200000
INDEX_NAME = "twitter_index"
DOC_TYPE = "twitter"




def kmeans_algo(es, k):
    points_arr = create_points_dict(es)
    print(points_arr)
    kmeans = KMeans(n_clusters=6, random_state=0).fit(points_arr)
    print(kmeans.cluster_centers_)




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
    return A














