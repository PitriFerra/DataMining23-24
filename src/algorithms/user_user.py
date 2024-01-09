import faiss
import numpy as np
from algorithms.dimensionality_reduction import cosine_similarity

def user_user_collaborative_filtering(u, std_route, k=5):     
    # convert None entries to 0.0 entries to avoid issues with the function cosine_similarity
    for i in range(len(u)):
        for j in range(len(u[0])):
            if u[i][j] is None:
                u[i][j] = 0.0

    similarity = [[0] * len(u) for _ in range(len(u))]

    #find k most similar users to each driver
    for i in range(len(u)):
        for j in range(len(u)):
            similarity[i][j] = (cosine_similarity(u[i], u[j]), j) # pair indicating distance similarity to driver j

    result = [[0] * k for _ in range(len(u))]
    
    for i in range(len(u)):
        # sort each users's row by the similarity to other users
        similarity[i].sort(key = lambda l: l[0], reverse=True)

        for j in range(len(u[0])):
            if u[i][j] == 0.0: # consider only unrated entries
                # take average rating given by the k similar users
                rank = 0.0
                for l in range(k):
                    rank += u[similarity[i][l][1]][j]
                u[i][j] = rank / k

    # convert u matrix to pair matrix where the second entry is the index of the route
    for i in range(len(u)):
        for j in range(len(u[0])):
            u[i][j] = (u[i][j], j)

    for i in range(len(u)):
        u[i].sort(key = lambda l: l[0], reverse=True) 
        res = []
        for l in range(k):
            res.append(u[i][l][1])
        
        result[i] = res
    
    return result