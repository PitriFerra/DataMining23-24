import numpy as np
import faiss
import unittest
from algorithms.dimensionality_reduction import cosine_similarity

def content_based_filtering(profile, route, k, lsh):
    '''
    Recommends k routes to each driver in profiles from the matrix route

    Arguments:
    profile: The profiles matrix
    route: The route profile matrix
    k: the number of routes to recommend to each driver
    lsh: Boolean indicating whether to use the lsh technique or not

    Returns:
    A matrix whith 5 indexes per driver in the profile matrix
    '''
    profile = np.array(profile)
    route = np.array(route)

    dimensions = len(route[0])
    nbits = 128
    result = [[0] * k for _ in range(len(profile))]

    if lsh:
        # hash all route using LSH
        index = faiss.IndexLSH(dimensions, nbits)
        index.add(route)

        # search for the k most similar route to each driver's profile
        for i in range(len(profile)):
            D, I = index.search(profile[i].reshape(1, dimensions), k)
            result[i] = I[0].tolist()
    else:
        for i in range(len(profile)):
            arr = []
            for j in range(len(route)):
                arr.append((cosine_similarity(profile[i], route[j]), j))

            arr.sort(key = lambda x: x[0]) 
            res = []
            for l in range(k):
                res.append(arr[l][1])

            result[i] = res

    return result


class TestBuildProfiles(unittest.TestCase):
    def test_filtering(self):
        # generate random n * d matrix
        n = 100
        d = 50
        D = np.random.rand(n, d)
        R = np.random.rand(n, d)
        
        res = content_based_filtering(D, R, 5, True)
        
        print(res[0]) # result for driver number 0

if __name__ == '__main__':
    unittest.main()