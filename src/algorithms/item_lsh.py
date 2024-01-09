import faiss
import numpy as np

'''
Function collaborative filtering item-item
It recommends routes to a driver with the implementation of lsh method
    u: utility matrix 
    std_route: vector of standard routes 
    k: number of routes  

Returns: 
    A matrix n * k, where n is the number of the drivers and k is the number of the recommended routes
'''

def item_item_lsh_collaborative_filtering(u, std_route, k=5):
    '''
    u = [[None, 1.0, 0.4, None, None],
        [None, None, 0.4, 0.4, 0.5],
        [1.4, 1.4, 2.0, None, None],
        [None, None, 2.1, 1.1, 1.3],
        [2.1, 0.5, 0.5, 0.5, None]]

    std_route = [[0.0, 1.0, 1.0, 0.5, 0.0],
                [0.1, 0.0, 1.0, 0.3, 0.1],
                [1.3, 0.0, 1.0, 0.0, 1.2],
                [0.3, 1.4, 1.0, 0.5, 0.0],
                [0.0, 1.2, 1.7, 0.0, 0.8],]
    '''
    std_route = np.array(std_route)
    dimensions = len(std_route[0])
    nbits = 128
    index = faiss.IndexLSH(dimensions, nbits)
    index.add(std_route)
    
    #print("BEFORE")
    #for i in range(len(u)):
    #    print(u[i])

    for i in range(len(u)):
        for j in range(len(u[0])):
            if u[i][j] is None:
                D, I = index.search(std_route[i].reshape(1, dimensions), k)
                # in I we have the index of std_route more similar 
                rank = 0
                contributions = 0
                for l in I[0]:
                    if u[i][l] is not None:
                        rank += u[i][l]
                        contributions += 1

                if contributions != 0:
                    u[i][j] = rank / contributions
                else: 
                    u[i][j] = 0

    #print("AFTER")
    #for i in range(len(u)):
    #    print(u[i])

    result = [[0] * k for _ in range(len(u))]

    # convert u matrix to pair matrix where the second entry is the index of the route
    for i in range(len(u)):
        for j in range(len(u[0])):
            u[i][j] = (u[i][j], j)
    
    #print("AFTER CONVERSION")
    #for i in range(len(u)):
    #    print(u[i])

    for i in range(len(u)):
        u[i].sort(key = lambda l: l[0], reverse=True) 
        res = []
        for l in range(k):
            res.append(u[i][l][1])
        
        result[i] = res

    #print("RESULT SORT")
    for i in range(len(result)):
        print(result[i])
    
    return res