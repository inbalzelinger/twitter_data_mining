#“coordinates” attributes is formatted as [LONGITUDE, latitude],
#“geo” attribute is formatted as [latitude, LONGITUDE].

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans



def kmeans_algo(es, k, country_bounding):
    X, y_true = make_blobs(n_samples=300, centers=4,
                           cluster_std=0.60, random_state=0)
    plt.scatter(X[:, 0], X[:, 1], s=50)
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);


    # coordinate_dict = create_points_dict(es)
    # random_points = pick_up_k_random_points(k, country_bounding, coordinate_dict)
    # print(random_points)


def create_points_dict(es):
    coordinate_dict = {}
    i = 0
    res = es.search(index='twitter_index', doc_type="twitter", body={"size":'10000',"query": {"match_all":{}}})
    for tweet in res['hits']['hits']:
        if tweet["_source"] is not None:
            if 'coordinates' in tweet["_source"]:
                if tweet["_source"]['coordinates'] is not None:
                    i += 1
                    print(tweet["_source"]['coordinates'])
                    coordinate_dict[tweet["_source"]["id_str"]] = tweet["_source"]['coordinates']

    #print(i)
    #print(coordinate_dict)
    return coordinate_dict

def pick_up_k_random_points(k, country_bounding, coordinate_dict):
    k_points_arry = np.arry()
    k_dict = {key: coordinate_dict[key] for key in list(coordinate_dict)[:k]}
    #print(k_dict)
    for key, val in k_dict.items():
        k_points_arry.append(val['coordinates'])
    #print(k_points_arry)
    return k_points_arry













