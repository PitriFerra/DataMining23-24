from build_route_vector import route_to_vector
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(vec1, vec2):
    vec1_values = []
    vec2_values = []
    copy = vec2.copy()

    for key in vec1.keys():
        vec1_values.append(vec1[key])
        vec2_values.append(0)

        for key2 in vec2.keys():
            if(key == key2):
                vec2_values[-1] = copy.pop(key2)
                break
                

    for key in copy.keys():
        vec2_values.append(vec2[key])
        vec1_values.append(0)

    #cosine similarity between two vectors -> Pietro's function
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