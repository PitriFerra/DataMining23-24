#from ..data.generate_std_routes import generate_random_route

def edit_merch(trip_merch, product, feature):
    if(product in trip_merch):
        trip_merch[product] = int((trip_merch[product] + feature[1]) / 2)
    else:
        trip_merch[product] = feature[1]

def get_best_routes(profiles, features, max_quantity, max_rating):
    routes_part_3 = []

    for profile in profiles:
        routes_part_3.append(get_best_route(profile, features, max_quantity, max_rating))

    return routes_part_3

def get_best_route(profile, features, max_elements, max_rating):
    best = {}
    avg = 0
    cnt = 0
    route = []
    cities = [] # This is used to check whether a feature features a city that is already added to the route
    route.append({"from": "", "to": "", "merchandise": {}})

    for feature in profile:
        if(feature > 0):
            avg += feature
            cnt += 1

    if cnt != 0:
        avg /= cnt

        for index, feature in enumerate(profile):
            if(feature > avg):
                best[next((key for key, value in features.items() if value == index), None)] = (feature, int(feature * max_elements / max_rating))

        route = []
        cities = [] # This is used to check whether a feature features a city that is already added to the route
        route.append({"from": "", "to": "", "merchandise": {}})

        for feature in best:
            city, from_to, product = feature

            if(city in cities):
                if(route[0]["from"] == city):
                    if(from_to):
                        edit_merch(route[0]["merchandise"], product, best[feature])
                    else:
                        route.insert(0, {"from": "", "to": city, "merchandise": {product: best[feature][1]}})
                else:
                    found = False
                    i = 0

                    while not found and i < len(route):
                        if(route[i]["to"] == city):
                            found = True
                        else:
                            i += 1
                    
                    if(from_to):
                        if(len(route) - 1 > i):
                            edit_merch(route[i + 1]["merchandise"], product, best[feature])
                        else:
                            route.append({"from": city, "to": "", "merchandise": {product: best[feature][1]}})
                    else:
                        edit_merch(route[i]["merchandise"], product, best[feature])
            else:
                cities.append(city)

                if(from_to):
                    if(route[0]["from"] == ""):
                        route[0]["from"] = city
                        edit_merch(route[0]["merchandise"], product, best[feature])
                    else:
                        route.insert(0, {"from": city, "to": route[0]["from"], "merchandise": {product: best[feature][1]}})
                else:
                    if(route[-1]["to"] == ""):
                        route[-1]["to"] = city
                        edit_merch(route[-1]["merchandise"], product, best[feature])
                    else:
                        route.append({"from": route[-1]["to"], "to": city, "merchandise": {product: best[feature][1]}})
        
    if route[0]["from"] == "":
        route[0]["from"] = next(iter(features))[0]

    if route[-1]["to"] == "":
        route[-1]["to"] = next(iter(features))[0]

    return route
'''
def part3_baseline(driver):
    return {
        "driver_id": driver,
        "route": generate_random_route()
    }
'''