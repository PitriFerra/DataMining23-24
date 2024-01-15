import numpy as np
import random
from algorithms.build_profiles import build_profiles
from algorithms.build_utility_matrix import build_utility_matrix
from algorithms.build_utility_matrix import build_utility_matrix_dict
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
from collections import OrderedDict

def main(argv):
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

    # cluster users and output recommended routes
    if str(sys.argv).__contains__("-p1"):
        centroids = kmeans_cluster(profiles, len(profiles), reduce_dimensions=True, plot=True) 
        centroids_to_routes(centroids, len(std_routes), features, max_quantity)

    # ##### PART2 #####
    if str(sys.argv).__contains__("-p2"):
        if str(sys.argv).__contains__("-user_user"):
            # user-user
            result = user_user_lsh_collaborative_filtering(u, k=5, lsh=False)
        
        elif str(sys.argv).__contains__("-item_item"):
            # item-item
            u_dict = build_utility_matrix_dict(standard_data, actual_data, drivers, features)
            result = item_item_collaborative_filtering(u_dict, k=5)  
        
        elif str(sys.argv).__contains__("-user_user_lsh"):
            # user user + LSH
            result = user_user_lsh_collaborative_filtering(u, std_routes, 5)
        
        elif str(sys.argv).__contains__("-content_based"):
            # content based
            result = content_based_filtering(profiles, std_routes, k=5, lsh=False)

        elif str(sys.argv).__contains__("-content_based_lsh"):
            # content based + LSH
            result = content_based_filtering(profiles, std_routes, k=5, lsh=True)

        elif str(sys.argv).__contains__("-hybrid"):
            # # hybrid 
            item_item_lsh = item_item_lsh_collaborative_filtering(u, std_routes, k=5)
            content_based_lsh = content_based_filtering(profiles, std_routes, k=5, lsh=True)
            result = hybrid_filtering(item_item_lsh_collaborative_filtering, content_based_lsh)
        
        else:
            # item_item + LSH
            result = item_item_lsh_collaborative_filtering(u, std_routes, k=5)

        output_recommended_routes(result)
    
    # ##### PART3 #####
    if str(sys.argv).__contains__("-p3"):
        results = []
        i = 1
        
        for profile in profiles:
            results.append({"driver": f"d{i}", "route": get_best_route(profile, features, max_quantity, max_rating)})
            i += 1

        with open('perfectRoute.json', 'w') as json_file:
            json.dump(results, json_file, indent=2)
    
    
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
    
def centroids_to_routes(centroids, m, features, max_quantity):
    results = []
    count = 1

    for _ in range(int(m / len(centroids))):
        tmp = centroids.copy()

        for i in range(len(centroids)):
            max_rating = 0

            for j in range(len(centroids[0])):
                tmp[i][j] += tmp[i][j] / 100 * random.randint(-5, 5) # add/sub +/- 5%

                if tmp[i][j] > max_rating:
                    max_rating = tmp[i][j]
            
            results.append({"id": f"s{count}", "route": get_best_route(tmp[i], features, max_quantity, max_rating)})
            count += 1
            
    with open("recStandard.json", "w") as f:
        json.dump(results, f, indent = 2)

def output_recommended_routes(result):
    output = []

    for index, solution in enumerate(result):
        output.append({"driver": f"d{index + 1}", "routes": [f"s{route}" for route in solution]})

    with open('driver.json', 'w') as json_file:
        json.dump(output, json_file, indent=2)

if __name__ == '__main__':
    main(sys.argv[1:]) 