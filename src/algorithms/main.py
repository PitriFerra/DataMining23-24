import numpy as np
import random
from build_profiles import build_profiles
from build_utility_matrix import build_utility_matrix
from cluster import kmeans_cluster
from build_route_vector import route_to_vector
from item_item import item_item_collaborative_filtering 
import json
from part3 import get_best_route

def main():
    ###### PART1 #####
    # read all JSON routes and transfrom them into feature vectors
    with open('standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)

    with open('actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
        
    std_routes = [route_to_vector(item["route"]) for item in standard_data]
    act_routes = [route_to_vector(item["route"]) for item in actual_data]    
        
    drivers = set()
    for route in actual_data:
        drivers.add(route["driver"])

    n = len(drivers)
    m = len(act_routes)
    
    # build utility matrix
    u = build_utility_matrix(standard_data, actual_data, drivers)
        
    # build user profiles
    # profiles = build_profiles(u, act_routes, n, m, len(std_routes[0]))
    
    # TO DELETE #
    n = 4000       
    d = 150
    density = 20
    profiles = np.random.rand(n, d)
    
    for i in range(n):
        for j in range(d):
            if random.randint(1,100) > density:
                profiles[i][j] = 0.0
    # TO DELETE #

    # cluster users
    centroids = kmeans_cluster(profiles, len(profiles)) 
    
    # output JSON recommended standard routes
    with open("recStandard.json", "w") as f:
        for _ in range(int(len(std_routes) / len(centroids))):
            tmp = centroids.copy()
            for i in range(len(centroids)):
                for j in range(len(centroids[0])):
                    tmp[i][j] += tmp[i][j] / 100 * random.randint(-5, 5) # add/sub +/- 5%
                json.dump(get_best_route(tmp), f)
        
    # ##### PART2 #####
        
    # # user-user
    
    # # item-item  
    # item_item = item_item_collaborative_filtering(u, n=5)  

    # # content based

    # # hybrid 
        

    # ##### PART3 #####
    # part3 = get_best_route(profiles)
    # print(part3)

if __name__ == '__main__':
    main() 