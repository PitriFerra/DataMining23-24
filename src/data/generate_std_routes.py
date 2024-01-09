import json
import random

#### Path of json file ####
path_locations = 'locations.json' #path of the file with the list of locations
path_items = 'items.json' #path of the file with the list of items
path_driver_attr = 'driver_attributes.json' #path of the file with the driver_attributes
path_standard = 'standard.json' #path of the output of the standard routes json file

#### Parameters ####
n_locations = 20 #number of locations from the json file 
n_items = 8 #number of items from the json file
n_std_routes = 1000 #number of standard routes to create 

with open(path_locations, 'r', encoding='utf-8') as locations_file:
    locations = json.load(locations_file)[:n_locations]
with open(path_items, 'r', encoding='utf-8') as items_file:
   items = json.load(items_file)[:n_items]

def generate_merchandise():
    merchandise = {}
    for _ in range(random.randint(1, 5)):
        product = random.choice(items) 
        quantity = random.randint(1, 20)
        merchandise[product] = quantity
    return merchandise

def generate_random_route():
    selected_locations = random.sample(locations, random.randint(4, 6))
    route = []

    for i in range(len(selected_locations) - 1):
        route.append({
            "from": selected_locations[i],
            "to": selected_locations[i + 1],
            "merchandise": generate_merchandise()
        })

    return route

data = []

for i in range(n_std_routes): 
    data.append({
        "id": f"s{i+1}",
        "route": generate_random_route()
    })
    
with open(path_standard, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)