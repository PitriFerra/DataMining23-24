import numpy as np
import unittest
import random
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn import preprocessing
from dimensionality_reduction import svd
from kneed import KneeLocator
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt


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
        dimensions = len(profile[0])
        # dimensionality reduction
        profile, model = svd(profile, dimensions, 0.1)
        
    # normalize input so that the cosine distance is proportional to the square of the euclidian distance
    profile, norms = preprocessing.normalize(X=profile, axis=0, return_norm=True)
        
    k =  2                                    
    prev_inertia = None
    curr_inertia = None
    delta_inertia = 1.0
    kmeans = None
    if plot:
        err = []
        ks = []
    
    while (delta_inertia > 0.1 and k < len(profile) / 2): 
        kmeans = KMeans(n_clusters = k, n_init="auto").fit(profile)
        if plot:
            err.append(kmeans.inertia_)
            ks.append(k)
        
        k *= 2
        prev_inertia = curr_inertia
        curr_inertia = kmeans.inertia_
        if prev_inertia is not None:
            delta_inertia = (prev_inertia - curr_inertia) / prev_inertia
    
    if plot:
        plt.plot(ks, err)
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
    profile = None
    model = None
    
    # dimensionality reduction
    if reduce_dimensions: 
        dimensions = len(profile[0])
        # dimensionality reduction
        profile, model = svd(profile, dimensions, 0.1)
        
    # min_samples = 2 * #dimensions according to a popular heuristic in the Sander et. al paper (1998)
    min_samples = min(2 * len(profile[0]), len(profile))
    
    #knn to find elbow point
    neighbors = NearestNeighbors(n_neighbors=min_samples)
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
    
    return DBSCAN(eps=kneedle.elbow_y, min_samples=2*len(profile[0]), metric="cosine").fit(profile)
    
'''
Unit tests 
'''
class TestBuildProfiles(unittest.TestCase): 
    def test_kmeans_cluster(self):
        n = 500   
        d = 10
        density = 30
        S = np.random.rand(n, d)
        
        for i in range(n):
            for j in range(d):
                if random.randint(1,100) > density:
                    S[i][j] = 0.0
        kmeans_cluster(S, n, True, True)
    
    def testDBSCAN(self):
        n = 200   
        d = 15
        density = 20
        S = np.random.rand(n, d) 
        
        DBSCAN_cluster(S, reduce_dimensions=True, plot=True)
        
if __name__ == '__main__':
    unittest.main()