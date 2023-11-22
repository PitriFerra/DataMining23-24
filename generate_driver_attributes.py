import json
import random

def generate_merchandise():
    merchandise = {}
    for _ in range(random.randint(1, 5)):
        product = random.choice(["milk", "pens", "butter", "honey", "tomatoes", "bread"])
        quantity = random.randint(1, 20)
        merchandise[product] = quantity
    return merchandise

def generate_location_pair_elements(locations):
    pair_elements = []
    
    for i in range(len(locations)):
        for j in range(len(locations)):
            if locations[i] != locations[j]:
                pair_elements.append({
                    "from": locations[i],
                    "to": locations[j],
                    "merchandise": generate_merchandise()
                })
    return pair_elements

data = []

# Generate elements for location pairs
locations = ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]

for i in range(10): # Ask the professor what would be a good number for standard and actual routes
    data.append({
        "id": f"d{i+1}",
        "probabilities": {
            "cityError": random.random(),
            "merchandiseError": random.random(),
            "merchandiseError2": random.random()
        },
        "preferences": generate_location_pair_elements(locations)
    })

with open('driver_attributes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
