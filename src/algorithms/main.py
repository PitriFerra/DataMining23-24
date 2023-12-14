import build_profiles
from  build_utility_matrix import build_utility_matrix
from cluster import kmeans_cluster
from build_route_vector import route_to_vector
from item_item import item_item_collaborative_filtering 
import json
from part3 import get_best_route

def main():
    print("hello :D")
    ###### PART1 #####
    # read all JSON routes and transfrom them into feature vectors
    with open('standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)

    with open('actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
        
    std_features_vectors = []
    act_features_vectors = []
    drivers = set()
        
    for route in standard_data:
        std_features_vectors.append(route_to_vector(route["route"]))

    for route in actual_data:
        act_features_vectors.append(route_to_vector(route["route"]))
        drivers.add(route["driver"])

    n = len(drivers)
    m = len(actual_data)
        
    # build utility matrix
    u = build_utility_matrix(std_features_vectors, act_features_vectors)
    
    # build user profiles
    profiles = build_profiles(u, actual_data, n, m, len(profiles[0]))

    # cluster users
    clusters = kmeans_cluster(profiles, profiles.len())
    
    # output JSON routes from the centroids
    get_best_route(clusters) # NOTE: only outputs one route per centroid!

    ##### PART2 #####
        
    # user-user
    
    # item-item  
    item_item = item_item_collaborative_filtering(u, n=5)  

    # content based

    # hybrid 
        

    ##### PART3 #####
    part3 = get_best_route(profiles)
    print(part3)

if __name__ == '__main__':
    main() 