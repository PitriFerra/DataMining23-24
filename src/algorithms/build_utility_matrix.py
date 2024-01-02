from build_route_vector import route_to_vector
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
        return np.nan

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

def build_utility_matrix(s_data, a_data, drivers):
    #initialization None 
    utility_matrix = {driver: {route['id']: None for route in s_data} for driver in drivers}

    for standard_route in s_data:
        for actual_route in a_data:
            #if there is a match, it means we have corresponding routes 
            if actual_route['sroute'] == standard_route['id']:
                #assign the driver from standard_route to the variable 'driver'
                driver = actual_route['driver']
                
                #convert routes to feature vectors = Pietro's function
                standard_vector = route_to_vector(standard_route['route'])
                actual_vector = route_to_vector(actual_route['route'])
                
                #calculate cosine similarity and update the utility matrix with the rating 
                similarity = calculate_cosine_similarity(standard_vector, actual_vector)
                utility_matrix[driver][standard_route['id']] = similarity

    return utility_matrix