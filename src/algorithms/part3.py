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



profiles = build_profiles(u, item, n, m, features)

for profile in profiles:
    