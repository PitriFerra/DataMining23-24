from sklearn.cluster import KMeans
import unittest

'''
    Clusters the user's profiles using the Kmeans algorithm.

    Arguments:
    profile: The user's profiles 
    n: The number of users

    Complexity: 
    time: O(n * k^2 * T)

    Returns:
    The centroids
'''
def kmeans_cluster(profile, n):
    clusters = 4
    prev_inertia = 0.0
    curr_inertia = 0.0
    kmeans = None
    
    while (not (curr_inertia * 1.15 < prev_inertia) and clusters < n): # while inertia decreases by less than 15%
        kmeans = KMeans(n_clusters = clusters, n_init="auto").fit(profile)
        prev_inertia = curr_inertia
        curr_inertia = kmeans.inertia_
        clusters *= 2        
            
    return kmeans.cluster_centers_

'''
Unit tests 
'''
class TestBuildProfiles(unittest.TestCase): 
    def test(self):
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