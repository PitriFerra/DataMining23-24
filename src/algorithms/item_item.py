'''
Function collaborative filtering item-item
It recommends items to a user based on the similarity of items that the user has liked 
    u: utilty matrix 
    n: number of routes 
    d: driver to recommend the routes 
    d_rating: the rating of each route of the driver  
    unrated_routes: the routes where the rating is None = the driver never made/rated it 
'''
def item_item_collaborative_filtering(u, n=5):
    all_recommendations = [] 

    for d, d_rating in u.items():
        #list of routes never rated/made by driver 
        unrated_routes = []
        for route, rating in d_rating.items():
            if rating is None: 
                unrated_routes.append(route)

        #recomendations based on routes similarity 
        recommendations = {}
        for unrated_route in unrated_routes:
            route_similarities = {}
            for route, _ in d_rating.items():
                if unrated_route != route and d_rating[unrated_route] is None:
                    #cosine similarity between the rating of the driver and all the other ratings 
                    similarity = calculate_cosine_similarity(u[unrated_route], d_rating)
                    route_similarities[route] = similarity

            #sort recommended routes in ascending order
            sorted_similarities = sorted(route_similarities.items(), key=lambda x: x[1], reverse=True)

            #take the top 5 recommended routes
            top_r = []
            for route, _ in sorted_similarities[:n]:
                top_r.append(route) 
            
            recommendations[unrated_route] = top_r
        all_recommendations.append({'driver': d, 'routes': recommendations})

    return all_recommendations