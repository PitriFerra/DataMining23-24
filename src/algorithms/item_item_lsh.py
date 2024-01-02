from build_utility_matrix import calculate_cosine_similarity
import faiss
import numpy as np

'''
Function collaborative filtering item-item with also the implementation of LSH

It recommends items to a user based on the similarity of items that the user has liked 
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
        routes = set()
        for driver_ratings in u.values():
            for route, rating in driver_ratings.items():
                if rating is not None:
                    routes.add(route) 
        routes = list(routes)
        drivers = list(u.keys())

        similarities = {}
        for route1 in routes:
            for route2 in routes:
                if route1 != route2:
                    #similarity between the routes
                    ratings_r1 = {}
                    for driver in drivers: 
                        ratings_r1[driver] = u[driver][route1]  
                    ratings_r2 = {}
                    for driver in drivers: 
                        ratings_r2[driver] = u[driver][route2]            
                    similarity = calculate_cosine_similarity(ratings_r1, ratings_r2) 
                    similarities[(route1, route2)] = similarity
        
        j = 0
        #rating for route None
        for driver in u:
            for route in u[driver]:
                if u[driver][route] is None:
                    j += 1
                    #find similar routes
                    other_routes = []
                    for other_route in routes:
                        if other_route != route:
                            other_routes.append(other_route)
                    similarity_key = lambda other_route: similarities.get((route, other_route), 0)
                    other_routes.sort(key=similarity_key, reverse=True)
                    similar_routes = other_routes[:k] 

                    #weighted avg 
                    num = 0
                    den = 0
                    for other_route in similar_routes:
                        similarity = similarities.get((route, other_route), 0)
                        rating = u[driver][other_route]
                        if rating is not None:
                            num = num + (similarity * rating)
                            den = den + abs(similarity) 


                    if den != 0:
                        estimated_rating = num / den
                        u[driver][route] = estimated_rating

        print(j)

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