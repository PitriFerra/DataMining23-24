import json
import random

def generate_merchandise():
    result = {}
    items = ["milk", "pens", "butter", "honey", "tomatoes", "bread"]
    merchandise = random.sample(items, len(items))
    
    for item in merchandise:
        result[item] = random.randint(1, 20)
    
    return result

data = []
locations = ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]

for i in range(10): # Ask the professor what would be a good number for standard and actual routes
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
            "merchandise": generate_merchandise()
        }
    })

with open('driver_attributes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
