import random

def edit_merch(merchandise, pref_merch, stubborness):
    merch = merchandise.copy()
    n_merch = len(pref_merch)

    for product in merch:
        bias = n_merch - pref_merch.index(product) # Every driver has a bias 
        # (for every product) which is relative to how much he likes a product 
        # (its position on pref_merch). The lower the position, the higher the bias, and the higher 
        # the bias, the lower the probability to divert from the standard route
        
        if random.random() < stubborness["del_merch"] / bias:
            merchandise.pop(product)
        elif random.random() < stubborness["edit_merch"] / bias:
            merchandise[product] = 30
    
    for product in pref_merch:
        if product not in merch and random.random() < stubborness["add_merch"] / (1 + pref_merch.index(product)):
            merchandise[product] = 30

def generate_merchandise(pref_merch, stubborness, items):
    result = {}
    merchandise = random.sample(items, len(items))
    
    for item in merchandise:
        result[item] = random.randint(1, 20)

    edit_merch(result, pref_merch, stubborness)
    return result

def modify_route(act_route, driver, items):
    stubborness = driver["stubborness"]
    pref_cities = driver["preferences"]["cities"]
    pref_merch = driver["preferences"]["merchandise"]
    n_cities = len(pref_cities)
    cities = [act_route[0]["from"]]

    for trip in act_route:
        if len(act_route) > 1 and random.random() < stubborness["del_city"] / (n_cities - pref_cities.index(trip["to"])):
            i = act_route.index(trip)
            
            if i < len(act_route) - 1:
                act_route[i - 1]["to"] = act_route[i + 1]["from"]
    
            act_route.remove(trip)
        else:
            cities.append(trip["to"])
            edit_merch(trip["merchandise"], pref_merch, stubborness)
    
    for city in pref_cities:
        if city not in cities and random.random() < stubborness["add_city"] / (1 + pref_cities.index(city)):
            route_length = len(act_route)
            pos = random.randint(0, route_length)
            act_route.insert(pos, 
                             {"from": city if pos != route_length else act_route[-1]["to"], 
                              "to": city if pos == route_length else act_route[pos]["from"], 
                              "merchandise": generate_merchandise(pref_merch, stubborness, items) if pos == 0 or pos == route_length else act_route[pos - 1]["merchandise"]})
            cities.append(city)

            if pos != 0 and pos != route_length:
                act_route[pos - 1]["to"] = city
                act_route[pos - 1]["merchandise"] = generate_merchandise(pref_merch, stubborness, items)
    
    return act_route