from algorithms.build_route_vector import route_to_vector
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import OrderedDict

def calculate_cosine_similarity(vec1, vec2):
    common_keys = set(vec1.keys()) & set(vec2.keys()) #common key between the two vectors 
    
    #similarity only for the routes with a rating 
    vec1_values = []
    for key in common_keys:
        if vec1[key] is not None:
            vec1_values.append(vec1[key])
    vec2_values = []
    for key in common_keys:
        if vec2[key] is not None:
            vec2_values.append(vec2[key])

    #if there are not values return Nan = no calculate cosine similarity 
    if not vec1_values or not vec2_values:
        return 0

    #the length of the vector has to be the same 
    for key in set(vec1.keys()) - common_keys:
        vec1_values.append(vec1[key])
        vec2_values.append(0)

    for key in set(vec2.keys()) - common_keys:
        vec1_values.append(0)
        vec2_values.append(vec2[key])

    max_len = max(len(vec1_values), len(vec2_values))
    vec1_values += [0] * (max_len - len(vec1_values))
    vec2_values += [0] * (max_len - len(vec2_values))

    #cosine similarity between two vectors 
    similarity = cosine_similarity([vec1_values], [vec2_values])
    return similarity.item()

def build_utility_matrix(s_data, a_data, drivers, features):
    utility_matrix = []

    for driver in drivers:
        utility_matrix.append([None] * len(s_data))

    for actual_route in a_data:
        #if there is a match, it means we have corresponding routes 
        driver_index = int(actual_route['driver'][1:]) - 1
        std_index = int(actual_route['sroute'][1:]) - 1
        std_route = s_data[int(actual_route['sroute'][1:]) - 1]
        std_vec = route_to_vector(std_route['route'], features)
        act_vec = route_to_vector(actual_route['route'], features)

        for i in std_vec:
            if std_vec[i] == 0 and act_vec[i] == 0:
                std_vec.pop(i)
                act_vec.pop(i)

        utility_matrix[driver_index][std_index] = cosine_similarity([std_vec], [act_vec]).item()

    return utility_matrix