import faiss
import numpy as np

def user_user_lsh_collaborative_filtering(u, std_route, k=5):    
    # convert None entries to 0.0 entries to avoid issued with FAISS
    for i in range(len(u)):
        for j in range(len(u[0])):
            if u[i][j] is None:
                u[i][j] = 0.0

    u = np.array(u)
    dimensions = len(u[0])
    nbits = 128
    index = faiss.IndexLSH(dimensions, nbits)
    index.add(u)

    for i in range(len(u)):
        D, I = index.search(u[i].reshape(1, dimensions), k)  # find k most similar users
        for j in range(len(u)):
            if u[i][j] == 0.0:
                rank = 0.0
                contributions = 0
                for similar_user in I[0]:
                    if u[similar_user][j] is not None:
                        rank += u[similar_user][j]
                        contributions += 1
                if contributions != 0:
                    u[i][j] = rank / contributions
                else:
                    u[i][j] = 0.0

    # we have now filled the utility matrix => just output the best 5 items for each user
    result = [[0] * k for _ in range(len(u))]

    u = u.tolist()

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