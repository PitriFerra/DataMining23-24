import json
import random

data = []
locations = ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]
items = ["milk", "pens", "butter", "honey", "tomatoes", "bread"]

for i in range(100): # Ask the professor what would be a good number for standard and actual routes
    data.append({
        "id": f"d{i+1}",
        "stubborness": {
            "del_city": random.random(),
            "add_city": random.random(),
            "del_merch": random.random(),
            "add_merch": random.random(),
            "edit_merch": random.random()
        },
        "preferences": {
            "cities": random.sample(locations, len(locations)),
            "merchandise": random.sample(items, len(items))
        }
    })

with open('src/data/driver_attributes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
