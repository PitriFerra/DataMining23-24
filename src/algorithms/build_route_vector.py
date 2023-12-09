import json

'''
    Given a route, it computes the "vector" of its features.
    
    Arguments:
    r: the route containing trips and merchandise.
    dict: the dictionary that connects keys (as "Milano", ecc.) to values.

    Complexity:
    time: O(n_trips * m_products)
    space: No new variables in this function
    
    Returns:
    Nothing. The dictionary is passed for reference so there's no need to return anything.
'''
def route_to_vector(r):
    dict = {}

    for trip in r:
        for product in trip["merchandise"]:
            dict[(trip["from"], True, product)] = trip["merchandise"][product]
            dict[(trip["to"], False, product)] = trip["merchandise"][product] 

    return dict


# Following lines for testing
with open('src/data/standard.json', 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

i = 0
dict = []

for route in standard_data:
    dict.append(route_to_vector(route["route"]))
    print(f"Feature vector of route {route["id"]} is {dict[-1]}")
    i += 1