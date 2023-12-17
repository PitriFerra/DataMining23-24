import unittest
import math
import random
import numpy as np
from sklearn.decomposition import TruncatedSVD

def svd(X, n, max_loss):
    '''
    Performs dimensionality reduction on the given matrix in such a way that the total information loss
    is less than max_loss
    
    Arguments:
    X: the input matrix
    n: the number of dimensions, i.e. the number of colums
    max_loss: The desired maximum loss
    
    Returns:
    The reduced matrix X    
    '''
    Y = None
    mid = None
    i = 1
    
    while i != n and n - i > 20:
        mid = int((i + n) / 2)
                
        svd = TruncatedSVD(n_components=mid, random_state=42)
        Y = svd.fit_transform(X)
        loss = information_loss(X, svd.inverse_transform(Y)) 
        if loss < max_loss:
            n = mid
        else:
            i = mid + 1

    print("reduced to ", mid, " dimensions")
    return Y, svd

def information_loss(X, Y):
    '''
    Given two matrices X and Y, where Y is the reconstructed X matrix, it calculates the difference in terms of the average 
    cosine distance between all the elements
    
    Arguments:
    X: The first matrix
    Y: The second reconstructed matrix 
    NOTE: It does not matter which matrix is the reconstructed one, the function will work anyway
    
    Complexity:
    time: O(n * m), where n and m are respectively the number of rows and columns
    
    Returns:
    The total information loss, in a number between 0 and 1, where 0.32 means 33% of informations were lost
    '''
    delta = 0.0
    for i in range(len(X)):
        delta += 1 - cosine_similarity(X[i], Y[i])
    return delta / (2 * len(X))


def cosine_similarity(X, Y):
    '''
    Given two lists, it calculates the cosine similarity between them
    
    Arguments:
    X: The first list
    Y: The second list
    
    Complexity:
    time: O(n * m), where n and m are respectively the number of rows and columns
    
    Returns:
    The cosine similarity, i.e. a number between -1 and 1
    
    '''
    product = 0.0
    n1 = 0.0
    n2 = 0.0
    
    for i in range(len(X)):
        product += X[i] * Y[i]
        n1 += X[i] * X[i] 
        n2 += Y[i] * Y[i]
        
    if n1 == 0.0 or n2 == 0.0:
        return 1.0
        
    return product / (math.sqrt(n1) * math.sqrt(n2))

# Unit tests
class TestBuildProfiles(unittest.TestCase):             
    def test_information_loss(self):
        X1 = [[0.0, 1.0, 1.0, 0.5, 0.0],
                    [0.1, 0.0, 1.0, 0.3, 0.1],
                    [1.3, 0.0, 1.0, 0.0, 1.2],
                    [0.3, 1.4, 1.0, 0.5, 0.0],
                    [0.0, 1.2, 1.7, 0.0, 0.8],]
        X2 = [[0.0, 1.0, 1.0, 0.5, 0.0],
                    [0.1, 0.0, 1.0, 0.3, 0.1],
                    [1.3, 0.0, 1.0, 0.0, 1.2],
                    [0.3, 1.4, 1.0, 0.5, 0.0],
                    [0.0, 1.2, 1.7, 0.0, 0.8],]

        self.assertAlmostEqual(information_loss(X1, X2), 0.0)
    
    def test_cosine_similarity(self):
        # equal vectors
        X1 = [0.0, 1.0, 1.0, 0.5, 0.0]
        X2 = [0.0, 1.0, 1.0, 0.5, 0.0]
        self.assertAlmostEqual(1.0, cosine_similarity(X1, X2))
        
        # orthogonal vectors
        X1 = [0.0, 1.0, 0.0]
        X2 = [0.0, 0.0, 1.0]
        X3 = [1.0, 0.0, 0.0]
        self.assertAlmostEqual(0.0, cosine_similarity(X1, X2))
        self.assertAlmostEqual(0.0, cosine_similarity(X1, X3))
        self.assertAlmostEqual(0.0, cosine_similarity(X2, X3))        
        
        # opposite vectors
        X1 = [0.0, 1.0, 1.0, 0.5, 0.0]
        X2 = [0.0, -1.0, -1.0, -0.5, 0.0]
        self.assertAlmostEqual(-1.0, cosine_similarity(X1, X2))   
        
        #random vectors     
        X1 = [-0.5, 0.5, 0.5, 0.5, 1.5]
        X2 = [0.0, -1.0, -1.0, -0.5, 0.0]
        self.assertAlmostEqual(-0.462250163, cosine_similarity(X1, X2))   
        
        #null vectors
        X1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        X2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.assertAlmostEqual(1.0, cosine_similarity(X1, X2))   
    
    def test_svd(self):
        n = 400   
        d = 50
        density = 10
        S = np.random.rand(n, d)
        
        for i in range(n):
            for j in range(d):
                if random.randint(1,100) > density:
                    S[i][j] = 0.0
        
        svd(S, d, 0.2)
                
if __name__ == '__main__':
    unittest.main()