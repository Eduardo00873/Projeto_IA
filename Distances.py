import requests
from geopy.distance import geodesic
import math

def get_city_coordinates(cities, api_key):
    coordinates = {}
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    
    for city in cities:
        params = {"address": city, "key": api_key}
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                lat = data["results"][0]["geometry"]["location"]["lat"]
                lng = data["results"][0]["geometry"]["location"]["lng"]
                coordinates[city] = (lat, lng)
            else:
                coordinates[city] = "Not found"
        else:
            coordinates[city] = f"Error: {response.status_code}"
    
    return coordinates

def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def calculate_distances(coordinates):
    distances = {}
    cities = list(coordinates.keys())
    
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            city1, city2 = cities[i], cities[j]
            if isinstance(coordinates[city1], tuple) and isinstance(coordinates[city2], tuple):
                distance = haversine(coordinates[city1], coordinates[city2])
                distances[(city1, city2)] = distance
            else:
                distances[(city1, city2)] = "Not found"
    
    return distances

key = "AIzaSyAl0Kl6-Z44AG8k5KBQlJH9ThesXzRG-KE"
cities = ["Lisboa", "Aveiro", "Faro", "Viseu"]
coordinates = get_city_coordinates(cities, key)
distances = calculate_distances(coordinates)
print(distances)


