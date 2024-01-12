import json
import random
from data.generate_std_routes import generate_random_route
from data.generate_act_routes import modify_route

#### Path of json files ####
path_locations = 'data/locations.json' #path of the file with the list of locations
path_items = 'data/items.json' #path of the file with the list of items
path_driver_attr = 'data/driver_attributes.json' #path of the file with the driver_attributes
path_standard = 'data/standard.json' #path of the output of the standard routes json file
path_actual = 'data/actual.json' #path of the output of the actual routes json file 

#### Parameters ####
n_locations = 20 #number of locations from the json file 
n_items = 8 #number of items from the json file
n_std_routes = 1000 #number of standard routes to create 
n_drivers = 400 #number of drivers
x = 0.15 #how much to fill the utility matrix

std = []
drivers = []
act = []

with open(path_locations, 'r', encoding='utf-8') as locations_file:
    locations = json.load(locations_file)[:n_locations]

with open(path_items, 'r', encoding='utf-8') as items_file:
    items = json.load(items_file)[:n_items] 

for i in range(n_std_routes): 
    std.append({
        "id": f"s{i+1}",
        "route": generate_random_route(items, locations)
    })

print("Generated std routes.")

for i in range(n_drivers):
    upper_bound = random.randint(0, 10) / 10
    lower_bound = random.randint(0, 10) / 10

    drivers.append({
        "id": f"d{i+1}",
        "stubborness": {
            "del_city": random.uniform(lower_bound, upper_bound),
            "add_city": random.uniform(lower_bound, upper_bound),
            "del_merch": random.uniform(lower_bound, upper_bound),
            "add_merch": random.uniform(lower_bound, upper_bound),
            "edit_merch": random.uniform(lower_bound, upper_bound)
        },
        "preferences": {
            "cities": random.sample(locations, len(locations)),
            "merchandise": random.sample(items, len(items))
        }
    })

print("Generated drivers.")
element_id = 1

for driver in drivers:
    for standard in std:
        if random.random() < x:
            actual_element = {
                "id": f"a{element_id}",
                "driver": driver["id"],
                "sroute": standard["id"],
                "route": modify_route(standard["route"], driver, items)
            }            
            act.append(actual_element)
            element_id += 1

print("Generated act routes.")
with open(path_standard, 'w', encoding='utf-8') as f:
    json.dump(std, f, ensure_ascii=False, indent=4)

with open(path_driver_attr, 'w', encoding='utf-8') as f:
    json.dump(drivers, f, ensure_ascii=False, indent=4)

with open(path_actual, 'w', encoding='utf-8') as f:
    json.dump(act, f, ensure_ascii=False, indent=4)