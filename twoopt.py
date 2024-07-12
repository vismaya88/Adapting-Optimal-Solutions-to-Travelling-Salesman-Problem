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

# 2-opt algorithm to improve the given path
def tsp_2opt(points, path):
    def swap_2opt(route, i, k):
        new_route = route[:i] + route[i:k+1][::-1] + route[k+1:]
        return new_route

    best_path = path
    best_distance = total_distance(path, points)
    n = len(path)
    improved = True

    start_time = time.time()

    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_path = swap_2opt(best_path, i, k)
                new_distance = total_distance(new_path, points)
                if new_distance < best_distance:
                    best_path = new_path
                    best_distance = new_distance
                    improved = True

    end_time = time.time()
    execution_time = end_time - start_time

    return best_path, best_distance, execution_time

# Function to list available datasets
def list_datasets(folder):
    files = [f for f in os.listdir(folder) if f.endswith('.txt')]
    return files

# Function to read a dataset from a file
def read_dataset(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                x, y = map(float, line.split()[:2])  # Only consider the first two values
                points.append((x, y))
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
    return points
