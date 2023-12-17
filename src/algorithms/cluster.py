import numpy as np
import unittest
import random
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn import preprocessing
from dimensionality_reduction import svd

def kmeans_cluster(profile, n):
    '''
        Clusters the user's profiles using the Kmeans algorithm.

        Arguments:
        profile: The user's profiles 
        n: The number of users

        Complexity: 
        time: O(n * k^2 * T). k is the number of clusters of the final model, whereas T is the average number of steps
        the algorithm takes to converge (Actually we stop after 10 iterations)

        Advantages:
        - The algorithm outputs centroids which are very convenient for the scope of this project

        Disadvantages:
        - Can be too slow for massive amounts of data
        - Clusters can only be circles
        - Only works for euclidian distance

        Returns:
        The centroids
    '''
    dimensions = len(profile[0])
    # dimensionality reduction
    profile, model = svd(profile, dimensions, 0.15)
    
    # normalize input so that the cosine distance is proportional to the square of the euclidian distance
    profile, norms = preprocessing.normalize(profile, axis=0, return_norm=True)
    
    k =  2                                    
    prev_inertia = None
    curr_inertia = None
    delta_inertia = 1.0
    kmeans = None
    
    while (delta_inertia > 0.05): 
        kmeans = KMeans(n_clusters = k, n_init="auto").fit(profile)
        k *= 2
        
        prev_inertia = curr_inertia
        curr_inertia = kmeans.inertia_
        if prev_inertia is not None:
            delta_inertia = (prev_inertia - curr_inertia) / prev_inertia
            
        print("k = ", k)
        print("current inertia = ", curr_inertia)
        print("previous inertia = ", prev_inertia)
        print("delta_inertia = ", delta_inertia)
        print("\n")
                
    return model.inverse_transform(kmeans.cluster_centers_ * norms)   #inverse transform of normalized clusters
'''
    Clusters the user profiles using the DBSCAN algorithm
    
    Arguments:
    profile: The user's profiles 
    n: The number of users
    
    Complexity:
    time: O(n * logn)
    space: O(n)
    
    Returns: 
    The label to which each cluster belongs
    
    Advantages:
    - Very good in terms of performance and computational complexity
    - Works with cosine similarity
    
    Disadvantages:
    - Adjusting the parameters on unkown data can be very tricky
    - The above complexity claims hold only for carefully chosen parameters
    - The output consists of labelled points, this is not optimal for the scope of this project
'''
def DBSCAN_cluster(profile):
    # eps: The maximum distance between two samples for one to be considered as in the neighborhood of the other. 
    # min_samples: The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. 
    clustering = DBSCAN(eps=3, min_samples=2, metric="cosine").fit(profile).labels_

'''
    Clusters the user profiles using the hierarchical clustering algorithm
    
    Arguments:
    profile: The user's profiles 
    n: The number of users
    
    Complexity:
    time: O(n^2 * logn)
    space: O(1)
    
    Returns: 
    The label to which each cluster belongs
    
    Advantages:
    - The clusters are of high quality
    - The clusters can be of any shape
    
    Disadvantages:
    - For massive amounts of data the algorithm is way too slow!
'''
def hierarchical_clustering(profile):
    clustering = AgglomerativeClustering().fit(profile).labels_
'''
Unit tests 
'''
class TestBuildProfiles(unittest.TestCase): 
    def test_kmeans_cluster(self):
        n = 2000   
        d = 150
        density = 20
        S = np.random.rand(n, d)
        
        for i in range(n):
            for j in range(d):
                if random.randint(1,100) > density:
                    S[i][j] = 0.0
        kmeans_cluster(S, n)
                
if __name__ == '__main__':
    unittest.main()