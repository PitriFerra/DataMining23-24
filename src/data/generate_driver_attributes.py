import json
import random

data = []
locations = ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]
items = ["milk", "pens", "butter", "honey", "tomatoes", "bread"]

for i in range(100):
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

with open('src/data/driver_attributes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
