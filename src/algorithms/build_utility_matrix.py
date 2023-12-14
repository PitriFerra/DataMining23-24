import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def calculate_cosine_similarity(vec1, vec2):
    #convert dictionaries to vectors
    vec1_values = np.array(list(vec1.values()))
    vec2_values = np.array(list(vec2.values()))

    #cosine similarity between two vectors -> Pietro's function
    similarity = cosine_similarity([vec1_values], [vec2_values])
    return similarity.item()

def build_utility_matrix(standard_routes, actual_routes):
    #initialization None 
    utility_matrix = {driver: {route: None for route in routes} for driver in drivers}

    for standard_route in standard_routes:
        for actual_route in actual_routes:
            #if there is a match, it means we have corresponding routes 
            if standard_route['sroute'] == actual_route['id']:
                #assign the driver from standard_route to the variable 'driver'
                driver = standard_route['driver']
                
                #convert routes to feature vectors = Pietro's function
                standard_vector = route_to_vector(standard_route['route'])
                actual_vector = route_to_vector(actual_route['route'])
                
                #calculate cosine similarity and update the utility matrix with the rating 
                similarity = calculate_cosine_similarity(standard_vector, actual_vector)
                utility_matrix[driver][standard_route['sroute']] = similarity

    return utility_matrix