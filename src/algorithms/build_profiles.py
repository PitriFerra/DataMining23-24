import unittest
'''
    Given the utility matrix U, it computes the profile of each user.
    
    Arguments:
    u: The utility matrix
    item: The matrix of the item's features
    n: The number of users
    m: The number of routes
    features: The number of features in the profile array

    Complexity:
    time: O(n * m * features)
    space: O(2 * n * features)
    
    Returns:
    The profile of each driver, i.e. the vector of features of each driver
'''
def build_profiles(u, item, n, m, features):
    profile = [[0.0] * features for _ in range(n)]
    count = [[0.0] * features for _ in range(n)]
    avg = [0.0] * n

    # compute the average rating for each driver
    for i in range(n):
        cnt = 0
        for j in range(m):
            if u[i][j] is not None:
                cnt += 1
                avg[i] += u[i][j]
        if cnt != 0:
            avg[i] /= cnt
    
    for i in range(n):  
        for j in range(m):  
            rating = u[i][j]  
            if rating is not None:  
                for f in range(features):  
                    feature_weight = item[j][f]
                    if feature_weight != 0.0:   
                        profile[i][f] += (rating - avg[i]) * feature_weight 
                        count[i][f] += 1

    for i in range(n): 
        for f in range(features):  
            if count[i][f] != 0:
                profile[i][f] /= count[i][f]
                      
    return profile

'''
Unit tests 
'''
class TestBuildProfiles(unittest.TestCase):
    def test(self):
        #utility matrix
        u = [[None, 1.0, 0.4, None, None],
             [None, None, 0.4, 0.4, 0.5],
             [1.4, 1.4, 2.0, None, None],
             [None, None, 2.1, 1.1, 1.3],
             [2.1, 0.5, 0.5, 0.5, None]]
        #matrix of routes features
        item = [[0.0, 1.0, 1.0, 0.5, 0.0],
                [0.1, 0.0, 1.0, 0.3, 0.1],
                [1.3, 0.0, 1.0, 0.0, 1.2],
                [0.3, 1.4, 1.0, 0.5, 0.0],
                [0.0, 1.2, 1.7, 0.0, 0.8],]
        n = 5 #number of drivers
        m = 5 #number of routes
        features = 5 #number of features

        profiles = build_profiles(u, item, n, m, features)
        expected_first_row = [-0.18, 0.0, 0.0, 0.09, -0.165]
        expected_fifth_row = [-0.22666667, 0.32, 0.0, 0.093333333, -0.26]

        for i in range(n):
            self.assertAlmostEqual(expected_first_row[i], profiles[0][i])
            self.assertAlmostEqual(expected_fifth_row[i], profiles[4][i])

if __name__ == '__main__':
    unittest.main() 