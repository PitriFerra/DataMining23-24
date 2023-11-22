import json
import random
from copy import deepcopy

def modify_merchandise(merchandise, driver_merchandise):
    for product, quantity in driver_merchandise.items():
        if random.random() < 0.5:
            merchandise[product] = quantity

def modify_route(actual_element, driver):
    if random.random() < driver["probabilities"]["cityError"]:
        if random.random() < 0.5:
            actual_element["route"].pop(random.randint(0, len(actual_element["route"]) - 1))
            print(f"Driver {actual_element['driver']} skipped a city in route {actual_element['sroute']}")
        else:
            #actual_element["route"].insert(random.randint(0, len(actual_element["route"])), random.choice(deepcopy(driver))) To develop later
            print(f"Driver {actual_element['driver']} added wrong city in route {actual_element['sroute']}")
    
    for i in range(len(actual_element["route"])):
        if random.random() < driver["probabilities"]["merchandiseError"]:
            modify_merchandise(actual_element["route"][i]["merchandise"], driver["preferences"][i]["merchandise"])
            print(f"Driver {actual_element['driver']} added wrong item in route {actual_element['sroute']}")

        matching_preference = find_matching_preference(driver["preferences"], actual_element["route"][i]["from"], actual_element["route"][i]["to"])

        for product in actual_element["route"][i]["merchandise"].items():
            if random.random() < driver["probabilities"]["merchandiseError2"] and product in matching_preference:
                actual_element["route"][i]["merchandise"][product] = matching_preference[product]
                print(f"Driver {actual_element['driver']} loaded wrong number of item {product} in route {actual_element['sroute']}")

def find_matching_preference(driver_preferences, from_location, to_location):
    for preference in driver_preferences:
        if preference["from"] == from_location and preference["to"] == to_location:
            return preference["merchandise"]

def create_actual_element(driver, standard, element_id):
    actual_element = {
        "id": f"a{element_id}",
        "driver": driver["id"],
        "sroute": standard["id"],
        "route": deepcopy(standard["route"])
    }
    modify_route(actual_element, driver)
    return actual_element

# Load driver.json and standard.json
with open('driver_attributes.json', 'r', encoding='utf-8') as f:
    driver_data = json.load(f)

with open('standard.json', 'r', encoding='utf-8') as f:
    standard_data = json.load(f)

# Create actual.json data
actual_data = []
element_id = 1
for driver in driver_data:
    for standard in standard_data:
        actual_data.append(create_actual_element(driver, standard, element_id))
        element_id += 1

# Write actual.json
with open('actual.json', 'w', encoding='utf-8') as f:
    json.dump(actual_data, f, ensure_ascii=False, indent=4)