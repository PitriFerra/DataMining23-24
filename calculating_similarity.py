import json
import math

def get_cities(s):
    cities = [s[0]["from"]]

    for trip in s:
        cities.append(trip["to"])

    return cities

def calculateDistance(s, a, e):
    # Let's say k = 4. The more the average of cities added/deleted, the less the malus when somebody make a mistake
    # Let's assume that the added cities are the ones that have an empty merchandise
    wrong_cities = len(s) + 1
    #print(f"Cities to visit: {wrong_cities}")

    if a[0]["from"] == s[0]["from"]:
        #print(f"Visited a right city: {a[0]["from"]}")
        wrong_cities -= 1
    
    for trip in a:
        if trip["merchandise"] == None:
            #print(f"Visited a wrong city: {trip["from"] if a[0]["from"] != s[0]["from"] else trip["to"]}")
            wrong_cities += 1

        if trip["to"] in get_cities(s):
            #print(f"Visited a right city: {trip["to"]}")
            wrong_cities -= 1

    e.append(wrong_cities)
    return wrong_cities



with open('standard.json', 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

with open('actual.json', 'r', encoding='utf-8') as f:
    actual_data = json.load(f)

err = 0
errors = []

for a in range(len(actual_data)):
    err += calculateDistance(standard_data[a % 10]["route"], actual_data[a]["route"], errors)
    
k = err / len(actual_data)

for i in range(len(actual_data)):
    print(f"Similarity between {actual_data[i]["sroute"]} and {actual_data[i]["id"]} is e^(-1/{k} * {errors[i]}) = {math.exp(-1 / k * errors[i])}")