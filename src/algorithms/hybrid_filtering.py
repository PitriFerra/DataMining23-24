import numpy as np

def hybrid_filtering(collaborative, content, k):
    ''' 
    Recommends k routes to each driver

    Arguments:
    collaborative: The results from collaborative filtering
    content: The results from content based filtering
    k: the number of routes to recommend to each driver

    Returns:
    A matrix whith 5 indexes per driver in the profile matrix
    '''
    n = len(collaborative)
    m = len(collaborative[0])
    result = [[0] * k for _ in range(n)]

    for i in range(n):
        score = {}
        for j in range(m):
            if content[i][j] not in score:
                score[content[i][j]] = k - j
            else:
                score[content[i][j]] += k - j

            if collaborative[i][j] not in score:
                score[collaborative[i][j]] = k - j
            else:
                score[collaborative[i][j]] += k - j    
        sorted_score = sorted(score.items(), key=lambda x: x[1], reverse=True)

        res = [0] * k
        for l in range(k):
            res[l] = sorted_score[l][0]
        result[i] = res

    return result