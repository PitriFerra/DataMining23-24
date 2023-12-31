def find_routes(u, k=5):
    top_routes = []

    for driver, ratings in u.items():
        # Filtra solo le route con valori numerici (diverse da None)
        numeric_ratings = {}
        for route, rating in ratings.items():
            if rating is not None:
                numeric_ratings[route] = rating

        sorted_routes = sorted(numeric_ratings.items(), key=lambda x: x[1], reverse=True)

        driver_info = {
            'driver': driver, 
            'routes': [route for route, _ in sorted_routes[:k]]
        }

        top_routes.append(driver_info)

    return top_routes 