import numpy as np
import random
from algorithms.build_profiles import build_profiles
from algorithms.build_utility_matrix import build_utility_matrix
from algorithms.cluster import kmeans_cluster, DBSCAN_cluster
from algorithms.build_route_vector import route_to_vector
from algorithms.item_item import item_item_collaborative_filtering
from algorithms.item_lsh import item_item_lsh_collaborative_filtering
from algorithms.content_based_filtering import content_based_filtering
from algorithms.user_user import user_user_collaborative_filtering
from algorithms.user_user_lsh import user_user_lsh_collaborative_filtering
from algorithms.hybrid_filtering import hybrid_filtering
import json 
from algorithms.part3 import get_best_route
from algorithms.part3 import get_best_routes
import sys
import time 

# A Python program to demonstrate working of OrderedDict
from collections import OrderedDict

def main(argv):
    # read all JSON routes and transfrom them into feature vectors
    start_time = time.time()
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
        
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)

    features = def_features(standard_data, actual_data)
    std_routes = [route_to_vector(item["route"], features) for item in standard_data]
    act_routes = [route_to_vector(item["route"], features) for item in actual_data]    
    drivers = set()

    for route in actual_data:
        drivers.add(route["driver"])
    
    # # build utility matrix
    u = build_utility_matrix(standard_data, actual_data, drivers, features)
          
    # # build user profiles
    #profiles, max_rating = build_profiles(u, act_routes, len(u), len(u[0]), len(features))
    #max_quantity = max(max(row) for row in act_routes)

    ###### PART1 ###### 
    # # cluster users and output recommended routes
    #centroids = kmeans_cluster(profiles, len(profiles), reduce_dimensions=False, plot=False)  
    #centroids_to_routes(centroids, len(std_routes))
    #centroids_to_routes(centroids, len(std_routes), features, max_quantity, max_rating)
    
    ###### PART2 ######  
    # # item-item 
    #item_item = item_item_collaborative_filtering(u_dict, k=5)  

    # # item-item LSH  
    #item_item_lsh = item_item_lsh_collaborative_filtering(u, std_routes, k=5)

    # # user-user LSH
    #user_user_lsh = user_user_lsh_collaborative_filtering(u, std_routes, 5)

    # # user-user 
    # user_user = user_user_collaborative_filtering(u, std_routes, 5)
    
    # # content based
    # content_based = content_based_filtering(profiles, std_routes, k=5, lsh=True)

    # # hybrid 
    #item_item_lsh = item_item_lsh_collaborative_filtering(u, std_routes, k=5)
    #content_based = content_based_filtering(profiles, std_routes, k=5, lsh=True)
    #hybrid = hybrid_filtering(content_based, item_item_lsh, 5)
    
    end_time = time.time()
    print("start time = ", start_time, " end_time = ", end_time)
    print(end_time - start_time)

def def_features(std_data, act_data):
    features = OrderedDict()
    cities = set()
    products = set()
    i = 0
    
    for r in std_data:
        for trip in r["route"]:
            if trip["merchandise"] is not None:
                for product in trip["merchandise"]:
                    cities.add(trip["from"])
                    cities.add(trip["to"])
                    products.add(product)
    
    for r in act_data:
        for trip in r["route"]:
            if trip["merchandise"] is not None:
                for product in trip["merchandise"]:
                    cities.add(trip["from"])
                    cities.add(trip["to"])
                    products.add(product)

    for city in cities:
        for product in products:
            features[(city, True, product)] = i
            i += 1
            features[(city, False, product)] = i
            i += 1
    
    return features 

'''
def centroids_to_routes(centroids, m, features, max_quantity, max_rating):
    with open("recStandard.json", "w") as f:
        for _ in range(int(m / len(centroids))):
            tmp = centroids.copy()
            for i in range(len(centroids)):
                for j in range(len(centroids[0])):
                    tmp[i][j] += tmp[i][j] / 100 * random.randint(-5, 5) # add/sub +/- 5%
                json.dump(get_best_route(tmp, features, max_quantity, max_rating), f)
'''

if __name__ == '__main__':
    main(sys.argv[1:]) 