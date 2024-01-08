#!
import json
from build_route_vector import route_to_vector
from build_utility_matrix import calculate_cosine_similarity
from main import def_features
from ..data.generate_act_routes import modify_route
from ..data.generate_std_routes import generate_random_route

def part3():
    with open('part3.json', 'r', encoding='utf-8') as f:
        part3 = json.load(f)
    with open('driver_attributes.json', 'r', encoding='utf-8') as f:
        drivers = json.load(f)
    with open('actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
    with open('standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
    similarity = []
    features = def_features(standard_data, actual_data)

    for driver in drivers:
        standard_route = generate_random_route()
        similarity.append([calculate_cosine_similarity(route_to_vector(standard_route, features), 
                                                       route_to_vector(modify_route(standard_route, driver),
                                                                       features))])
    
    print(similarity)
    '''
    for solution in part3:
        modify_route(solution["route"], drivers[i])
        i += 1
    '''