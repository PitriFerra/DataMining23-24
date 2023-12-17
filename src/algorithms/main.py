from build_profiles import build_profiles
from  build_utility_matrix import build_utility_matrix
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
    print(std_routes)
    
        
    drivers = set()
    for route in actual_data:
        drivers.add(route["driver"])

    n = len(drivers)
    m = len(act_routes)
    
    # build utility matrix
    u = build_utility_matrix(standard_data, actual_data, drivers)
        
    # build user profiles
    profiles = build_profiles(u, act_routes, n, m, len(std_routes[0]))

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