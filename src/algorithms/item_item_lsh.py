from algorithms.build_utility_matrix import calculate_cosine_similarity
import faiss
import numpy as np

'''
Function collaborative filtering item-item with also the implementation of LSH

It recommends routes to a driver based on the similarity of pair of routes that the driver has liked 
    u: utility matrix 
    k: number of routes 
    lsh: if False, it uses cosine similarity; if True, it uses the LSH method 

Returns: 
    A matrix n * k, where n is the number of the drivers and k is the number of the recommended routes
'''

def item_item_lsh_collaborative_filtering(u, k=5, lsh=False): 
    
    if lsh: 
        #Method = LSH 
        routes = set()
        for driver_ratings in u.values():
            for route, rating in driver_ratings.items():
                if rating is not None:
                    routes.add(route)
        routes = list(routes)
        drivers = list(u.keys())
        d = len(u[next(iter(u))])  #len of the vector for each driver 
        nbits = 128
        index = faiss.IndexLSH(d, nbits)
        route_vectors = [list(u[driver].get(route) for route in routes) for driver in u]  #ratings vector
        index.add(np.array(route_vectors, dtype='float32'))  #add the ratings vector to the LSH index

        #find similar routes
        for driver in u:
            for route, rating in u[driver].items():
                if rating is None: 
                    r_index = routes.index(route)
                    r_vec = np.array(route_vectors[r_index], dtype='float32')  #ratings vector for the route with value None
                    D, I = index.search(np.array([r_vec], dtype='float32'), k + 1)  #use the LSH index to find similar vectors to route_vec
                    sim_routes = [i for i in I[0] if i != r_index] 
                    #print(sim_routes) 

                    for route in u[driver]:
                        if u[driver][route] is None:  #if rating is None 
                            #find the similar rating between the similar drivers 
                            similar_ratings = []
                            for i in sim_routes: 
                                if u[drivers[i]][route] is not None:
                                    similar_ratings.append(u[drivers[i]][route])

                            #avg of the ratings 
                            if similar_ratings:
                                estimated_rating = np.mean(similar_ratings)
                                u[driver][route] = estimated_rating
        #return u
    else:
        #Method = Cosine Similarity 
        drivers = list(u.keys())
        routes = set()
        for driver in drivers:
            for route, _ in u[driver].items():
                #if rating is not None:
                routes.add(route) 
        routes = list(routes)
        #print(routes)
        #print(drivers)

        route_pairs = set()
        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):
                route1 = routes[i]
                route2 = routes[j]
                route_pairs.add((route1, route2)) 
        #print(route_pairs) 

        similarities = {}
        for route1 in routes:
            for route2 in routes:
                if route1 != route2:
                    pair_key = (route1, route2)
                    similarities[pair_key] = {}

                    #similarity between the routes
                    ratings_r1 = {}
                    ratings_r2 = {}
                    for driver in drivers: 
                        rating1 = u[driver].get(route1)  
                        rating2 = u[driver].get(route2)  

                        if rating1 is not None and rating2 is not None: 
                            ratings_r1[driver] = rating1
                            ratings_r2[driver] = rating2
                               
                    similarity = calculate_cosine_similarity(ratings_r1, ratings_r2) 
                    similarities[(route1, route2)] = similarity
        #print(similarities)

        #rating for route None
        for driver in u:
            for route in u[driver]:
                if u[driver][route] is None:
                    num = 0.0
                    den = 0.0
                    for r in u[driver]:
                        if u[driver][r] is not None:  
                            similarity = similarities[(route, r)] 
                            num += similarity * u[driver][r] 
                            den += similarity
                    if den != 0:
                        estimated_rating = num / den
                        u[driver][route] = estimated_rating
        #return u

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