import json

'''
    Given a route, it computes the vector of its features.
    
    Arguments:
    r: the route containing trips and merchandise.
    vec: the dictionary that connects keys (as "Milano", ecc.) to values.

    Complexity:
    time: O(n_trips * m_products)
    space: No new variables in this function
    
    Returns:
    Nothing. The dictionary is passed for reference so there's no need to return anything.
'''
def route_to_vector(r, vec):
    vec[r[0]["from"]] = 1

    for trip in r:
        vec[trip["to"]] = 1

        for product in trip["merchandise"]:
            vec[product] += trip["merchandise"][product]

# Following lines to create the features vector
vec = {}

for product in ["milk", "pens", "butter", "honey", "tomatoes", "bread"]:
    vec[product] = 0

for city in ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]:
    vec[city] = 0

# Following lines for testing
with open('src/data/standard.json', 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

for route in standard_data:
    vec_copy = vec.copy()
    route_to_vector(route["route"], vec_copy)
    print(f"Feature vector of route {route["id"]} is {vec_copy}")