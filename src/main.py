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
    start_time = time.time()
    # ##### PART1 #####
    # read all JSON routes and transfrom them into feature vectors
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
        
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)

    features = def_features(standard_data, actual_data)
    std_routes = [route_to_vector(item["route"], features) for item in standard_data]
    act_routes = [route_to_vector(item["route"], features) for item in actual_data]   
    max_quantity = max(max(row) for row in act_routes) 
    drivers = set()

    for route in actual_data:
        drivers.add(route["driver"])
    
    # build utility matrix
    u = build_utility_matrix(std_routes, act_routes, actual_data, drivers)
    #u = transform_utility_matrix(u_dict)
          
    # build user profiles
    profiles, max_rating = build_profiles(u, act_routes, len(u), len(u[0]), len(features))
    '''
    # cluster users and output recommended routes
    if str(sys.argv).__contains__("-dbscan"):
        dbscan = DBSCAN_cluster(profiles, reduce_dimensions=False, plot=False)
        labels_to_routes(dbscan, len(std_routes))
    else:
        centroids = kmeans_cluster(profiles, len(profiles), reduce_dimensions=True, plot=True) 
        centroids_to_routes(centroids, len(std_routes), features, max_quantity)
    '''

    # ##### PART2 #####
    # # user-user collaborative filtering with implementation of LSH
    #result = user_user_lsh_collaborative_filtering(u_dict, k=5, lsh=False)
    #print(user_user)  
    
    # # item-item collaborative filtering
    #result = item_item_collaborative_filtering(u_dict, k=5)  
    #print(item_item)

    # # item_item collaborative filtering with LSH  
    result = item_item_lsh_collaborative_filtering(u, std_routes, k=5)
    #print(item_item_lsh)  

    # user user collaborative filtering with LSH
    #result = user_user_lsh_collaborative_filtering(u, std_routes, 5)
    # print(user_user_lsh_collaborative_filtering)

    # user user collaborative filtering without LSH
    #result = user_user_collaborative_filtering(u, std_routes, 5)
    # print(user_user)
    
    # # content based
    #result = content_based_filtering(profiles, std_routes, k=5, lsh=True)

    # # hybrid 
    #result = item_item_collaborative_filtering(u_dict,5)
    
    # ##### PART3 #####
    results = []
    i = 1
    
    for profile in profiles:
        results.append({"driver": f"d{i}", "route": get_best_route(profile, features, max_quantity, max_rating)})
        i += 1

    with open('solutions/perfectRoute.json', 'w') as json_file:
        json.dump(results, json_file, indent=2)
    end_time = time.time()
    print(end_time - start_time)
    
    
def dict_to_vec(std_routes, act_routes, features):
    vec_std_routes = [[0] * len(features) for _ in range(len(std_routes))]
    vec_act_routes = [[0] * len(features) for _ in range(len(act_routes))]
    i = 0

    for r in std_routes:
        for feature in r:
            vec_std_routes[i][features[feature]] = std_routes[i][feature]
        i += 1
    
    i = 0
    for r in act_routes:
        for feature in r:
            vec_act_routes[i][features[feature]] = act_routes[i][feature]
        i += 1
            
    return vec_std_routes, vec_act_routes

def transform_utility_matrix(u_dict):
    u = []
    
    for driver in u_dict.keys():
        u.append([])

        for route in u_dict[driver].keys():
            u[-1].append(u_dict[driver][route]) 
    return u

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

def labels_to_routes(dbscan, m):
    if len(dbscan.components_) != 0:
        # naive approach: output one route per core point
        with open("recStandard.json", "w") as f:
            for i in range(int(m / len(dbscan.components_))):
                print("hola")
                #json.dump(get_best_route(dbscan.components_), f) 
    
def centroids_to_routes(centroids, m, features, max_quantity):
    results = []

    for _ in range(int(m / len(centroids))):
        tmp = centroids.copy()

        for i in range(len(centroids)):
            max_rating = 0

            for j in range(len(centroids[0])):
                tmp[i][j] += tmp[i][j] / 100 * random.randint(-5, 5) # add/sub +/- 5%

                if tmp[i][j] > max_rating:
                    max_rating = tmp[i][j]
            
            for solution in get_best_routes(tmp, features, max_quantity, max_rating):
                results.append(solution)
        
    with open("solutions/recStandard.json", "w") as f:
        json.dump(results, f, indent = 2)

if __name__ == '__main__':
    main(sys.argv[1:]) 