import numpy as np
import random
from build_profiles import build_profiles
from build_utility_matrix import build_utility_matrix
from cluster import kmeans_cluster, DBSCAN_cluster
from build_route_vector import route_to_vector
#from part2 import find_routes
#from user_user_lsh import user_user_lsh_collaborative_filtering 
#from item_item_lsh import item_item_lsh_collaborative_filtering 
import json 
from part3 import get_best_route
from part3 import get_best_routes
import sys

def main(argv):
    ###### PART1 #####
    # read all JSON routes and transfrom them into feature vectors
    with open('standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)

    with open('actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)

    std_routes = [route_to_vector(item["route"]) for item in standard_data]
    act_routes = [route_to_vector(item["route"]) for item in actual_data]    
        
    features = def_features(standard_data, actual_data)
    vec_std_routes, vec_act_routes = dict_to_vec(std_routes, act_routes, features)

    drivers = set()
    for route in actual_data:
        drivers.add(route["driver"])
    
    # build utility matrix
    u_dict = build_utility_matrix(standard_data, actual_data, drivers)
    u = transform_utility_matrix(u_dict)
          
    # build user profiles
    profiles, max_rating = build_profiles(u, vec_act_routes, len(u), len(u[0]), len(features))
    
    # cluster users and output recommended routes
    if str(sys.argv).__contains__("-dbscan"):
        dbscan = DBSCAN_cluster(profiles, reduce_dimensions=False, plot=False)
        labels_to_routes(dbscan, len(std_routes))
    else:
        centroids = kmeans_cluster(profiles, len(profiles), reduce_dimensions=True, plot=True) 
        centroids_to_routes(centroids, len(std_routes))
        
    # ##### PART2 #####
    # # top5 routes with full utility matrix
    #part2 = find_routes(u, k=5) 
    #print(part2)

    # # user-user with implementation of LSH
    #user_user = user_user_lsh_collaborative_filtering(u, k=5, lsh=False)
    #print(user_user)  
    
    # # item-item with implementation of LSH
    #item_item = item_item_lsh_collaborative_filtering(u, k=5, lsh=False)  
    #print(item_item)

    # # content based

    # # hybrid 
        

    # ##### PART3 #####
    max_quantity = max(max(row) for row in vec_act_routes)
    results = []
    i = 1
    
    for profile in profiles:
        results.append({"id_driver": f"d{i}", "route": get_best_route(profile, features, max_quantity, max_rating)})
        i += 1

    # Write the results to a JSON file
    with open('part3.json', 'w') as json_file:
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
    features = {}
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
    
def centroids_to_routes(centroids, m):
    with open("recStandard.json", "w") as f:
        for _ in range(int(m / len(centroids))):
            tmp = centroids.copy()
            for i in range(len(centroids)):
                for j in range(len(centroids[0])):
                    tmp[i][j] += tmp[i][j] / 100 * random.randint(-5, 5) # add/sub +/- 5%
                #json.dump(get_best_route(tmp), f)

if __name__ == '__main__':
    main(sys.argv[1:]) 