import os
import random
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

# Simulated Annealing Algorithm
def simulated_annealing(points, T=10000, alpha=0.995, stopping_temp=1e-5, stopping_iter=1000):
    n = len(points)
    current_solution = list(range(n))
    random.shuffle(current_solution)
    best_solution = current_solution
    current_cost = total_distance(current_solution, points)
    best_cost = current_cost

    start_time = time.time()
    iter_count = 0

    while T > stopping_temp and iter_count < stopping_iter:
        new_solution = current_solution.copy()
        l = random.randint(2, n-1)
        i = random.randint(0, n-l)
        new_solution[i:(i+l)] = reversed(new_solution[i:(i+l)])
        new_cost = total_distance(new_solution, points)
        delta_E = new_cost - current_cost

        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
            current_solution = new_solution
            current_cost = new_cost

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        T *= alpha
        iter_count += 1

    end_time = time.time()
    execution_time = end_time - start_time

    return best_solution, best_cost, execution_time
