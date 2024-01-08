import json
import random

def generate_merchandise():
    merchandise = {}
    for _ in range(random.randint(1, 5)):
        product = random.choice(["milk", "pens", "butter", "honey", "tomatoes", "bread"])
        quantity = random.randint(1, 20)
        merchandise[product] = quantity
    return merchandise

def generate_random_route():
    locations = ["Rome", "Milan", "Verona", "Florence", "Naples", "Turin", "Bologna", "Palermo", "Genoa", "Bari", "Catania", "Venice", "Cagliari", "Syracuse", "Brescia", "Pisa", "Reggio Calabria", "Parma", "Modena"]
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

for i in range(10): # Ask the professor what would be a good number for standard and actual routes
    data.append({
        "id": f"s{i+1}",
        "route": generate_random_route()
    })
    
with open('standard.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)