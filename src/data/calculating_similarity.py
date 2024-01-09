import json
import math

def jaccard_similarity(dict1, dict2):
    intersection_size = sum(min(dict1.get(key, 0), dict2.get(key, 0)) for key in set(dict1) | set(dict2))
    union_size = sum(max(dict1.get(key, 0), dict2.get(key, 0)) for key in set(dict1) | set(dict2))

    if union_size == 0:
        return 0.0  # Avoid division by zero if both chests are empty

    similarity = intersection_size / union_size
    return similarity

def get_cities_to_visit(s):
    cities = [s[0]["from"]]

    for trip in s:
        cities.append(trip["to"])

    return cities

def calculateDistance(s, a, e, n):
    if a[0]["from"] == s[0]["from"]:
        #print(f"Visited a right city: {a[0]["from"]}")
        wrong_cities = len(s)
        _n = 1
    else:
        _n = 0
        wrong_cities = len(s) + 1

    #print(f"Cities to visit: {wrong_cities}")
    
    for trip in a:
        if trip["merchandise"] == None: # Let's assume that the added cities are the ones that have an empty merchandise
            #print(f"Visited a wrong city: {trip["from"] if a[0]["from"] != s[0]["from"] else trip["to"]}")
            wrong_cities += 1

        if trip["to"] in get_cities_to_visit(s):
            #print(f"Visited a right city: {trip["to"]}")
            wrong_cities -= 1
            _n += 1

    e.append(wrong_cities)
    n.append(_n)
    return wrong_cities

def updateSimilarity(s, a, sim, pos, n):
    max = sim[pos] / n

    for trip in a:
        if trip["merchandise"] != None:
            sim[pos] -= max * (1 - jaccard_similarity(next((item.get("merchandise", {}) for item in s if item.get("to") == trip["to"]), None), trip["merchandise"]))


with open('standard.json', 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

with open('actual.json', 'r', encoding='utf-8') as f:
    actual_data = json.load(f)

k = 0
errors = []
n = []
sim = []

for i in range(len(actual_data)):
    k += calculateDistance(standard_data[i % 10]["route"], actual_data[i]["route"], errors, n)
    
k /= len(actual_data)

for i in range(len(actual_data)):
    sim.append(math.exp(-1 / k * errors[i]))
    print(f"Similarity between {actual_data[i]["sroute"]} and {actual_data[i]["id"]} is e^(-1/{k} * {errors[i]}) = {sim[i]}")
    updateSimilarity(standard_data[i % 10]["route"], actual_data[i]["route"], sim, i, n[i])
    print(f"Updated similarity between {actual_data[i]["sroute"]} and {actual_data[i]["id"]} is {sim[i]}")