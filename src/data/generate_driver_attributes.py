import json
import random

#### Path of json file ####
path_locations = 'locations.json' #path of the file with the list of locations
path_items = 'items.json' #path of the file with the list of items
path_driver_attr = 'driver_attributes.json' #path of the output of driver_attributes json file 

#### Parameters ####
n_locations = 20 #number of locations from the json file 
n_items = 8 #number of items from the json file
n_drivers = 100 #number of drivers

with open(path_locations, 'r', encoding='utf-8') as locations_file:
    locations = json.load(locations_file)[:n_locations]

with open(path_items, 'r', encoding='utf-8') as items_file:
   items = json.load(items_file)[:n_items] 

data = []

for i in range(n_drivers):
    upper_bound = random.randint(0, 10) / 10
    lower_bound = random.randint(0, 10) / 10

    data.append({
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

with open(path_driver_attr, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
