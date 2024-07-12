import os
import math
import time

from matplotlib import pyplot as plt

# Function to calculate Euclidean distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Function to calculate total distance of a path
def total_distance(path, points):
    total = 0
    for i in range(len(path) - 1):
        total += distance(points[path[i]], points[path[i+1]])
    total += distance(points[path[-1]], points[path[0]])  # Return to starting point
    return total

# Nearest Neighbor algorithm to find an approximate shortest path
def tsp_nearest_neighbor(points):
    n = len(points)
    start_time = time.time()
    
    if n == 0:
        return [], 0, 0
    
    unvisited = set(range(n))
    current = 0
    path = [current]
    unvisited.remove(current)
    
    while unvisited:
        next_city = min(unvisited, key=lambda city: distance(points[current], points[city]))
        path.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    
    end_time = time.time()
    execution_time = end_time - start_time
    min_distance = total_distance(path, points)
    
    return path, min_distance, execution_time
