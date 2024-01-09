import numpy as np
import unittest
import random
from sklearn.cluster import KMeans, DBSCAN
from sklearn import preprocessing
from algorithms.dimensionality_reduction import svd
from kneed import KneeLocator
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


def kmeans_cluster(profile, n, reduce_dimensions, plot):
    '''
        Clusters the user's profiles using the Kmeans algorithm.

        Arguments:
        profile: The user's profiles 
        n: The number of users
        reduce_dimensions: Boolean indicating whether to reduce dimensionality
        plot: Boolean indicating whether to plot the data in a graph

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
    if reduce_dimensions: 
        profile, model = svd(profile, len(profile[0]), 0.1)
        
    # normalize input so that the cosine distance is proportional to the square of the euclidian distance
    profile, norms = preprocessing.normalize(X=profile, axis=0, return_norm=True)
    
    err = []
    ks = []
    k = 2
    step = int(len(profile) / 50) + 1
    
    while k < len(profile):
        print("k = ", k)
        kmeans = KMeans(n_clusters = k, n_init="auto").fit(profile)
        err.append(kmeans.inertia_)
        ks.append(k)
        k += step
        
    kneedle = KneeLocator(err, ks, S = 1.0, curve="convex", direction="decreasing")
    if plot:
        print("elbow = ", kneedle.elbow_y)
        
        plt.plot(err, ks)
        plt.title("Sum of the quadratic distance from the closest centroid of all points in the kmeans algorithm")
        plt.ylabel("k")
        plt.xlabel("Distance")
        plt.show()
    
    if reduce_dimensions:                
        return model.inverse_transform(kmeans.cluster_centers_ * norms)   #inverse transform of normalized clusters
    else:
        return kmeans.cluster_centers_ * norms
'''
    Clusters the user profiles using the DBSCAN algorithm
    
    Arguments:
    profile: The user's profiles 
    n: The number of users
    reduce_dimensions: Boolean indicating whether to reduce dimensionality
    plot: Boolean indicating whether to plot the data in a graph
    
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
def DBSCAN_cluster(profile, reduce_dimensions, plot):   
    model = None
    
    # dimensionality reduction
    if reduce_dimensions: 
        dimensions = len(profile[0])
        # dimensionality reduction
        profile, model = svd(profile, dimensions, 0.1)
        
    # min_samples = 2 * #dimensions according to a popular heuristic in the Sander et. al paper (1998)
    min_samples = 2 * len(profile[0])
    if min_samples > len(profile):
        min_samples = int(len(profile) / 2)
    
    #knn to find elbow point
    neighbors = NearestNeighbors(n_neighbors=min_samples, metric="cosine")
    neighbors_fit = neighbors.fit(profile)
    distances, indices = neighbors_fit.kneighbors(profile)
    distances = np.sort(distances, axis=0)
    distances = distances[:,1]
    
    index = [i for i in range(len(distances))]
    
    kneedle = KneeLocator(index, distances, S = 1.0, curve="convex", direction="increasing")
    if plot:
        print("elbow = ", kneedle.elbow_y)
        plt.plot(distances)
        plt.title("Sorted distance from the kth neighbor")
        plt.xlabel("Driver index")
        plt.ylabel("Distance")
        plt.show()
    
    return DBSCAN(eps=kneedle.elbow_y, min_samples=min_samples, n_jobs=-1, metric="cosine").fit(profile)
    
'''
Unit tests 
'''
class TestBuildProfiles(unittest.TestCase): 
    def test_kmeans_cluster(self):
        n = 500   
        d = 15
        density = 30
        S = np.random.rand(n, d)
        
        for i in range(n):
            for j in range(d):
                if random.randint(1,100) > density:
                    S[i][j] = 0.0
        kmeans_cluster(S, n, False, False)
    
    def testDBSCAN(self):
        n = 1100
        d = 20
        S = np.random.rand(n, d) 
        
        dbscan = DBSCAN_cluster(S, reduce_dimensions=False, plot=True)
        s = set()
        
        for el in dbscan.core_sample_indices_:
            s.add(el)
        
        print("#clusters = ", len(s))
        print("#points = ", len(S)) 
   
        
    def testDBSCAN_cluster_count(self):
        centers = [[2, 2], [-2, -2], [2, -2]]
        X, labels_true = make_blobs(
            n_samples=1000, centers=centers, cluster_std=0.4, random_state=0
        )

        X = StandardScaler().fit_transform(X)
        dbscan = DBSCAN_cluster(X, False, False)
        
        s = set()
        
        for el in dbscan.core_sample_indices_:
            s.add(el)  
        
            
if __name__ == '__main__':
    unittest.main()