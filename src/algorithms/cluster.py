import numpy as np
import unittest
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn import preprocessing
from dimensionality_reduction import svd
'''
    Clusters the user's profiles using the Kmeans algorithm.

    Arguments:
    profile: The user's profiles 
    n: The number of users

    Complexity: 
    time: O(n * k^2 * T). k is the number of clusters of the final model, whereas T is the average number of steps
    the algorithm takes to converge
    
    Advantages:
    - The algorithm outputs centroids which are very convenient for the scope of this project
    
    Disadvantages:
    - Can be too slow for massive amounts of data
    - Clusters can only be circles
    - Only works for euclidian distance

    Returns:
    The centroids
'''
def kmeans_cluster(profile, n):
    # dimensionality reduction
    profile, model = svd(profile, len(profile[0]), 0.15)
    
    # normalize input so that the cosine distance is proportional to the square of the euclidian distance
    profile, norms = preprocessing.normalize(profile, axis=0, return_norm=True)
    clusters = 4                                        
    prev_inertia = 0.0
    curr_inertia = 0.0
    kmeans = None
    
    while (not (curr_inertia * 1.15 < prev_inertia) and clusters < n): # while inertia decreases by less than 15%
        kmeans = KMeans(n_clusters = clusters, n_init="auto").fit(profile)
        prev_inertia = curr_inertia
        curr_inertia = kmeans.inertia_
        clusters *= 2      
    
    print(kmeans.cluster_centers_)  
            
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
        profiles = [[0.0, 1.0, 1.0, 0.5, 0.0],
                    [0.1, 0.0, 1.0, 0.3, 0.1],
                    [1.3, 0.0, 1.0, 0.0, 1.2],
                    [0.3, 1.4, 1.0, 0.5, 0.0],
                    [0.0, 1.2, 1.7, 0.0, 0.8],]
        expected_centroids_sum = [1.55, 2.4, 4.7, 0.8, 2.1]
        actual_centroids = kmeans_cluster(profiles, 5)
            
        for j in range(5):
            sum_here = 0
            for i in range(4):
                sum_here += actual_centroids[i][j]
            self.assertAlmostEqual(expected_centroids_sum[j], sum_here)
                
if __name__ == '__main__':
    unittest.main()