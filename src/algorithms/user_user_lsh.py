from build_utility_matrix import calculate_cosine_similarity
import faiss
import numpy as np

'''
Function collaborative filtering user-user with also the implementation of LSH 

It recommends routes to a driver based on the preferences and behaviors of other drivers who are similar to that driver
    u: utility matrix 
    k: number of routes 
    lsh: if False, it uses cosine similarity; if True, it uses the LSH method

Returns: 
    A matrix n * k, where n is the number of the drivers and k is the number of the recommended routes 
'''
def user_user_lsh_collaborative_filtering(u, k=5, lsh=False):  

    if lsh: 
        #Method = LSH
        drivers = sorted(list(u.keys()))
        d = len(u[drivers[0]])
        nbits = 128 
        index = faiss.IndexLSH(d, nbits)
        driver_vectors = [list(u[driver].values()) for driver in drivers] #vecotr for each driver
        index.add(np.array(driver_vectors, dtype='float32'))

        for driver in drivers:
            d_index = drivers.index(driver) #each driver index in d_index
            d_vec = np.array(driver_vectors[d_index], dtype='float32') #vector of the current driver d_index
            #print(d_vec)

            D, I = index.search(np.array([d_vec], dtype='float32'), k + 1) #find the nearest index I to the current driver
            #similar drivers to the current driver d_index 
            sim_drivers = []
            for i in I[0]:
                if i != d_index:
                    sim_drivers.append(i) 
            #print(sim_drivers)

            for route in u[driver]:
                if u[driver][route] is None:  #if rating is None 
                    #find the similar rating between the similar drivers 
                    similar_ratings = []
                    for i in sim_drivers :
                        if u[drivers[i]][route] is not None: 
                            similar_ratings.append(u[drivers[i]][route])

                    #avg of the ratings 
                    if similar_ratings:
                        estimated_rating = np.mean(similar_ratings)
                        u[driver][route] = estimated_rating 
        #return u
    else: 
        #Method = Cosine Similarity
        while any(None in ratings.values() for ratings in u.values()):
            drivers = sorted(list(u.keys()))
            similarities = {}

            for i in range(len(drivers)):
                for j in range(i + 1, len(drivers)):
                    driver1 = drivers[i]
                    driver2 = drivers[j]

                    #common routes between drivers != None 
                    common_routes = []
                    for route in u[driver1]:
                        if route in u[driver2] and u[driver1][route] is not None and u[driver2][route] is not None:
                            common_routes.append(route)
                    #print(common_routes) 

                    if common_routes: 
                        d1 = {}
                        for route in common_routes:
                            d1[route] = u[driver1][route]  
                        #print(d1)
                        d2 = {}
                        for route in common_routes:
                            d2[route] = u[driver2][route]
                        #print(d2)

                        #similarity between the rating of the common routes of d1 and d2 
                        similarity = calculate_cosine_similarity(d1, d2) 
                        similarities[(driver1, driver2)] = similarity
                    else: 
                        similarities[(driver1, driver2)] = None

            #find similar drivers and their similarity 
            similar_drivers = {}
            for (driver1, driver2), similarity in similarities.items():
                if similarity is not None:
                    if driver1 not in similar_drivers:
                        similar_drivers[driver1] = []
                    if driver2 not in similar_drivers:
                        similar_drivers[driver2] = []

                    similar_drivers[driver1].append((driver2, similarity))
                    similar_drivers[driver2].append((driver1, similarity))
            for driver in similar_drivers:
                similar_drivers[driver] = sorted(similar_drivers[driver], key=lambda x: x[1], reverse=True)
            #print(similar_drivers) 

            #find the route None 
            for driver in u: 
                routes_none = []
                for route in u[driver]: 
                    if u[driver][route] is None: 
                        routes_none.append(route)
                #print(routes_none)
                if routes_none:
                    num = 0.0
                    den = 0.0
                    #find the similar driver and the similarity for the driver with route None
                    for similar_driver, similarity in similar_drivers.get(driver, []):
                        for r in routes_none:
                            if r in u[similar_driver] and u[similar_driver][r] is not None:
                                #rating based on the weighted avg
                                num += similarity * u[similar_driver][r]
                                den += similarity

                    if den != 0:
                        estimated_rating = num / den 
                        u[driver][r] = estimated_rating 
        return u 
    
    result = np.zeros((len(drivers), k), dtype='U20')
    for i, driver in enumerate(drivers):
        sorted_items = sorted(u[driver].items(), key=lambda x: x[1], reverse=True)
        sorted_routes = [route[0] for route in sorted_items]

        #index of top k routes
        r_indices = [list(u[driver].keys()).index(route) for route in sorted_routes[:k]]
        result[i, :] = r_indices
        
        #name of top k routes
        #r_names = sorted_routes[:k]
        #result[i, :] = np.array(r_names, dtype='U20')

    return result  
    
'''
    result = {}
    for driver in drivers:
        sorted_items = sorted(u[driver].items(), key=lambda x: x[1], reverse=True)
        sorted_routes = [route[0] for route in sorted_items]

        result[driver] = {'top5 routes': sorted_routes[:k]} 

    return result 
'''