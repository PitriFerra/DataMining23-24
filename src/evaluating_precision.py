import json
from algorithms.build_route_vector import route_to_vector
from main import def_features
from sklearn.metrics.pairwise import cosine_similarity
from data.generate_act_routes import modify_route
from data.generate_std_routes import generate_random_route

def part1():
    return

def part2():
    return

def part3():
    n_locations = 57 #number of locations from the json file 
    n_items = 23 #number of items from the json file
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
    n_iterations = 100
    j = 0
    sum_success_rate = 0
    global_sum_similarity_recommended = 0
    global_sum_similarity_random = 0
    features = def_features(standard_data, actual_data)

    while j < n_iterations:
        similarity = []
        sum_similarity_random = 0

        for driver in drivers:
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
        j += 1
        print(f"Iteration {j} out of {n_iterations}. Success rate: {success_rate}%. Avg similarity for random routes: {round(sum_similarity_random / i, 2)}. Avg similarity for recommended routes: {round(sum_similarity_recommended / i, 2)}.")
        
    global_avg_similarity_random = global_sum_similarity_random / (j * i)
    global_avg_similarity_recommended = global_sum_similarity_recommended / (j * i)
    print(f"Average success rate: {sum_success_rate / j}%.")
    print(f"Global average similarity for random routes: {round(global_avg_similarity_random, 2)}")
    print(f"Global average similarity for recommended routes: {round(global_avg_similarity_recommended, 2)}")
    print(f"Similarity has been improved by {round(global_avg_similarity_recommended / global_avg_similarity_random * 100)}%")


part = 3

if part == 1:
    part1()
elif part == 2:
    part2()
elif part == 3:
    part3()