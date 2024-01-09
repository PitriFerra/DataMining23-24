import json
from algorithms.build_route_vector import route_to_vector
from main import def_features
from sklearn.metrics.pairwise import cosine_similarity
from data.generate_act_routes import modify_route
from data.generate_std_routes import generate_random_route

def part3():
    with open('solutions/part3.json', 'r', encoding='utf-8') as f:
        part3 = json.load(f)
    with open('data/driver_attributes.json', 'r', encoding='utf-8') as f:
        drivers = json.load(f)
    with open('data/actual.json', 'r', encoding='utf-8') as f:
        actual_data = json.load(f)
    with open('data/standard.json', 'r', encoding='utf-8') as f:
        standard_data = json.load(f)
    j = 0
    sum_success_rate = 0

    while j < 10:
        similarity = []
        features = def_features(standard_data, actual_data)

        for driver in drivers:
            standard_route = generate_random_route()
            similarity.append([cosine_similarity([route_to_vector(standard_route, features)],
                                                 [route_to_vector(modify_route(standard_route, driver), features)]).item()])

        print(similarity)
        i = 0
        successes = 0

        for solution in part3:
            similarity[i].append(cosine_similarity([route_to_vector(solution["route"], features)],
                                                   [route_to_vector(modify_route(solution["route"], drivers[i]), features)]).item())

            if similarity[i][1] > similarity[i][0]:
                successes += 1

            i += 1

        success_rate = successes * 100 / i
        sum_success_rate += success_rate
        print(similarity)
        print(f"Number of successes: {successes}. Success rate: {success_rate}%")
        j += 1

    print(f"Average success rate: {sum_success_rate / j}")
part3()