import random

def generate_merchandise(items):
    merchandise = {}
    for _ in range(random.randint(1, 5)):
        product = random.choice(items) 
        quantity = random.randint(1, 20)
        merchandise[product] = quantity
    return merchandise

def generate_random_route(items, locations):
    selected_locations = random.sample(locations, random.randint(4, 6))
    route = []

    for i in range(len(selected_locations) - 1):
        route.append({
            "from": selected_locations[i],
            "to": selected_locations[i + 1],
            "merchandise": generate_merchandise(items)
        })

    return route