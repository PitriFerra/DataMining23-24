def build_profiles(u, item, n, m, features):
    profile = [n][[0.0] * features]
    count = [n][[0.0] * features]  
    avg = [n]

    # compute the average rating for each driver
    for i in range(n):
        cnt = 0
        for j in range(m):
            if u[i][j] is not None:
                cnt += 1
                avg[i] += u[i][j]
        if cnt != 0:
            avg[i] /= cnt
    
    for i in range(n):  
        for j in range(m):  
            entry = u[i][j]  
            if entry is not None:  
                for f in range(features):  
                    feature_weight = item[j][f]
                    if feature_weight != 0.0:   
                        count[i][f] += feature_weight 
                        profile[i][f] += entry * feature_weight 

    for i in range(n): 
        for f in range(features):  
            if count[i][f] != 0: 
                profile[i][f] = (profile[i][f] - avg[i] * count[i][f]) / count[i][f] 
                      
    return profile

def edit_merch(trip_merch, keys, feature):
    if(keys[2] in trip_merch):
        trip_merch[keys[2]] = (trip_merch[keys[2]] + feature[1]) / 2
    else:
        trip_merch[keys[2]] = feature[1]

profiles = build_profiles(u, item, n, m, features)
routes_part_3 = []

for profile in profiles:
    best = []
    avg = 0

    for feature in profile:
        avg += profile[feature][0]

    avg /= len(profile)

    for feature in profile:
        if(profile[feature][0] > avg):
            best.append(feature)

    route = []
    cities = [] # This is used to check whether a feature features a city that is already added to the route

    for feature in best:
        keys = feature.keys()

        if(keys[0] in cities):
            if(route[0]["from"] == keys[0]):
                if(keys[1]):
                    edit_merch(route[0]["merchandise"], keys, best[feature])
                else:
                    route.insert(0, {"from": "", "to": keys[0], "merchandise": {keys[2]: best[feature[1]]}})
            else:
                found = False
                i = 0

                while not found or i < len(route):
                    if(route[i]["to"] == keys[0]):
                        found = True
                    else:
                        i += 1
                
                if(keys[1]):
                    if(len(route) - 1 > i):
                        edit_merch(route[i + 1]["merchandise"], keys, best[feature])
                    else:
                        route.append({"from": keys[0], "to": "", "merchandise": {keys[2]: best[feature][1]}})
                else:
                    edit_merch(route[i]["merchandise"], keys, best[feature])
        else:
            cities.append(keys[0])

            if(keys[1]):
                if(route[0]["from"] == ""):
                    route[0]["from"] = keys[0]
                    edit_merch(route[0]["merchandise"], keys, best[feature])
                else:
                    route.insert(0, {"from": keys[0], "to": route[0]["from"], "merchandise": {keys[2]: best[feature[1]]}})
            else:
                if(route[-1]["to"] == ""):
                    route[-1]["to"] = keys[0]
                    edit_merch(route[-1]["merchandise"], keys, best[feature])
                else:
                    route.append({"from": route[-1]["to"], "to": keys[0], "merchandise": {keys[2]: best[feature[1]]}})
    
    routes_part_3.append(route)

print(routes_part_3)