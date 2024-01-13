import copy
import json
from algorithms.build_route_vector import route_to_vector
from main import def_features
from data.generate_act_routes import modify_route
from data.generate_std_routes import generate_random_route
from algorithms.item_item import item_item_collaborative_filtering
from algorithms.item_lsh import item_item_lsh_collaborative_filtering
from algorithms.content_based_filtering import content_based_filtering
from algorithms.user_user import user_user_collaborative_filtering
from algorithms.user_user_lsh import user_user_lsh_collaborative_filtering
from algorithms.hybrid_filtering import hybrid_filtering
from algorithms.build_utility_matrix import build_utility_matrix
from algorithms.build_profiles import build_profiles
from algorithms.dimensionality_reduction import cosine_similarity
from algorithms.build_utility_matrix import build_utility_matrix_dict
import random
from algorithms.user_user_lsh import user_user_lsh_collaborative_filtering


def part2_rmsqd():
    n_locations = 20 #number of locations from the json file 
    n_items = 8 #number of items from the json file
    with open('data/driver_attributes.json', 'r', encoding='utf-8') as f:
        driver_attributes = json.load(f)
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
    with open('data/items.json', 'r', encoding='utf-8') as items_file:
        items = json.load(items_file)[:n_items] 

    features = def_features(standard_data, actual_data)
    std_routes = [route_to_vector(item["route"], features) for item in standard_data]
    act_routes = [route_to_vector(item["route"], features) for item in actual_data]    
    drivers = set()

    for route in actual_data:
        drivers.add(route["driver"])
    
    # build utility matrix
    u = build_utility_matrix(standard_data, actual_data, driver_attributes, features)
    u_first = u.copy()
    u_second = u.copy()

    # set to None a fourth of the utility matrix
    for i in range(int(len(u) / 4)):
        for j in range(int(len(u[0]) / 4)):
            u[i][j] = None
          
    # build user profiles
    profiles, max_rating = build_profiles(u, act_routes, len(u), len(u[0]), len(features))

    item_item_lsh_recommendations = item_item_lsh_collaborative_filtering(u_first, std_routes, k=5)
    random_recommendations = random_filtering(u_second, 5)
    #content_based_recommendations = content_based_filtering(profiles, std_routes, k=5, lsh=True)
    #hybrid_recommendations = hybrid_filtering(content_based_recommendations, item_item_lsh_recommendations, 5)
    #user_user_lsh_recommendations = user_user_lsh_collaborative_filtering(u, std_routes, k=5)
    #user_user_vanilla_recommendations = user_user_collaborative_filtering(u, std_routes, 5)

    print("RANDOM")
    print(random_recommendations)
    print("ITEM")
    print(item_item_lsh_recommendations)

def random_filtering(u, k):
    for i in range(len(u)):
        for j in range(len(u[0])):
            if u[i][j] is None:
                u[i][j] = random.uniform(-1.0, 1.0)

    return u

def part2():
    n_locations = 20 #number of locations from the json file 
    n_items = 8 #number of items from the json file
    n = 800 #number of drivers
    with open('data/driver_attributes.json', 'r', encoding='utf-8') as f:
        driver_attributes = json.load(f)
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
    with open('data/items.json', 'r', encoding='utf-8') as items_file:
        items = json.load(items_file)[:n_items] 

    features = def_features(standard_data, actual_data)
    std_routes = [route_to_vector(item["route"], features) for item in standard_data]
    act_routes = [route_to_vector(item["route"], features) for item in actual_data]    
    drivers = set()

    for route in actual_data:
        drivers.add(route["driver"])
    
    # build utility matrix
    #u = build_utility_matrix(standard_data, actual_data, driver_attributes, features)
    u = build_utility_matrix_dict(standard_data, actual_data, driver_attributes, features)

    # build user profiles
    #profiles, max_rating = build_profiles(u, act_routes, len(u), len(u[0]), len(features))

    #item_item_lsh_recommendations = item_item_lsh_collaborative_filtering(u, std_routes, k=5)
    #user_user_lsh_recommendations = user_user_lsh_collaborative_filtering(u, std_routes, k=5)
    #content_based_recommendations = content_based_filtering(profiles, std_routes, k=5, lsh=True)
    #hybrid_recommendations = hybrid_filtering(content_based_recommendations, user_user_lsh_recommendations, 5)
    #user_user_vanilla_recommendations = user_user_collaborative_filtering(u, std_routes, 5)
    item_item_recommendations = item_item_collaborative_filtering(u, 5)

    # random recommendation system
    random_rec = [[0] * 5 for _ in range(n)]
    for i in range(n):
        for j in range(5):
            random_rec[i][j] = random.randint(0, len(std_routes) - 1)

    print("Finished creating recommendation systems")

    '''
    print("ITEM VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, item_item_lsh_recommendations, random_rec, standard_data, items, features, std_routes)
    #print("USER VS RANDOM")
    #average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, user_user_lsh_recommendations, random_rec, standard_data, items, features, std_routes)
    print("CONTENT VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, content_based_recommendations, random_rec, standard_data, items, features, std_routes)
    print("HYHBRid VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, hybrid_recommendations, random_rec, standard_data, items, features, std_routes)

    print("ITEM VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, random_rec, item_item_lsh_recommendations, standard_data, items, features, std_routes)
    #print("USER VS RANDOM")
    #average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, user_user_lsh_recommendations, random_rec, standard_data, items, features, std_routes)
    print("CONTENT VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, random_rec, content_based_recommendations, standard_data, items, features, std_routes)
    print("HYHBRid VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, random_rec, hybrid_recommendations, standard_data, items, features, std_routes)
    '''
    print("CONTENT VS RANDOM")
    average_cosine_similarity_between_two_filtering_systems(n, driver_attributes, random_rec, item_item_recommendations , standard_data, items, features, std_routes)
    
    
    

def average_cosine_similarity_between_two_filtering_systems(n_drivers, driver_attributes, recommendations_one, recommendations_two, standard_data, items, features, std_routes):
    driver_count = 0
    score_one = [0.0] * n_drivers
    score_two = [0.0] * n_drivers

    for driver in driver_attributes:
        for recommendation in recommendations_one[driver_count]:
            recommended_route = standard_data[recommendation]["route"]
            recommended_actual_route = route_to_vector(modify_route(copy.deepcopy(recommended_route), driver, items), features)
            recommended_route = std_routes[recommendation]
            score_one[driver_count] += 1 - cosine_similarity(recommended_actual_route, recommended_route)

        for recommendation in recommendations_two[driver_count]:
            recommended_route = standard_data[recommendation]["route"]
            recommended_actual_route = route_to_vector(modify_route(copy.deepcopy(recommended_route), driver, items), features)
            recommended_route = std_routes[recommendation]
            score_two[driver_count] += 1 - cosine_similarity(recommended_actual_route, recommended_route)
        
        driver_count += 1

    for i in range(n_drivers):
        score_one[i] /= 5
        score_two[i] /= 5

    average_one = sum(score_one) / len(score_one)
    average_two = sum(score_two) / len(score_two)

    print("FIRST RECOMMENDATION SYSTEM AVERAGE COSINE DISTANCE: ", average_one)
    print("SECOND RECOMMENDATION SYSTEM AVERAGE COSINE DISTANCE: ", average_two)



def part3():
    n_locations = 20 #number of locations from the json file 
    n_items = 8 #number of items from the json file
    with open('solutions/part3.json', 'r', encoding='utf-8') as f:
        part3 = json.load(f)
    with open('data/driver_attributes.json', 'r', encoding='utf-8') as f:
        drivers = json.load(f)
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
    with open('data/locations.json', 'r', encoding='utf-8') as locations_file:
        locations = json.load(locations_file)[:n_locations]
    with open('data/items.json', 'r', encoding='utf-8') as items_file:
        items = json.load(items_file)[:n_items] 
    j = 0
    sum_success_rate = 0
    global_sum_similarity_recommended = 0
    global_sum_similarity_random = 0
    features = def_features(standard_data, actual_data)

    while j < 100:
        similarity = []
        sum_similarity_random = 0

        for driver in drivers:
            print(driver)
            standard_route = generate_random_route(items, locations)
            similarity.append([cosine_similarity([route_to_vector(standard_route, features)],
                                                 [route_to_vector(modify_route(standard_route, driver, items), features)]).item()])
            sum_similarity_random += similarity[-1][0]

        i = 0
        successes = 0
        sum_similarity_recommended = 0

        for solution in part3:
            similarity[i].append(cosine_similarity([route_to_vector(solution["route"], features)],
                                                   [route_to_vector(modify_route(solution["route"], drivers[i], items), features)]).item())
            sum_similarity_recommended += similarity[i][1]

            if similarity[i][1] > similarity[i][0]:
                successes += 1

            i += 1

        global_sum_similarity_recommended += sum_similarity_recommended
        global_sum_similarity_random += sum_similarity_random
        success_rate = successes * 100 / i
        sum_success_rate += success_rate
        #print(similarity)
        #print(f"Success rate: {success_rate}%. Avg similarity for random routes: {round(sum_similarity_random / i, 2)}. Avg similarity for recommended routes: {round(sum_similarity_recommended / i, 2)}.")
        j += 1

    global_avg_similarity_random = global_sum_similarity_random / (j * i)
    global_avg_similarity_recommended = global_sum_similarity_recommended / (j * i)
    #print(f"Average success rate: {sum_success_rate / j}%.")
    #print(f"Global average similarity for random routes: {round(global_avg_similarity_random, 2)}")
    #print(f"Global average similarity for recommended routes: {round(global_avg_similarity_recommended, 2)}")
    #print(f"Similarity has been improved by {round(global_avg_similarity_recommended / global_avg_similarity_random * 100)}%")


def transform_utility_matrix(u_dict):
    u = []
    
    for driver in u_dict.keys():
        u.append([])

        for route in u_dict[driver].keys():
            u[-1].append(u_dict[driver][route]) 
    return u

part = 3

if __name__ == '__main__':
    part2()