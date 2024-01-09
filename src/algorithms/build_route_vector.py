def route_to_vector(r, features):
    vec = [0] * len(features)
    
    for trip in r:
        for product in trip["merchandise"]:
            vec[features[(trip["from"], True, product)]] = trip["merchandise"][product]
            vec[features[(trip["to"], False, product)]] = trip["merchandise"][product] 

    return vec