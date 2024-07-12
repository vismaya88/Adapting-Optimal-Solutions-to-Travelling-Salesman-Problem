import os
import random
import math
import time
from itertools import combinations
from multiprocessing import Pool

from matplotlib import pyplot as plt

class GeneticAlgorithmTSP:
    def __init__(self, points, population_size=100, elite_size=10, mutation_rate=0.01, generations=1000):
        self.points = points
        self.population_size = population_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.distance_matrix = self.compute_distance_matrix()
    
    def compute_distance_matrix(self):
        """Precompute the distance matrix."""
        n = len(self.points)
        distance_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                dist = self.distance(self.points[i], self.points[j])
                distance_matrix[i][j] = dist
                distance_matrix[j][i] = dist
        return distance_matrix
    
    def initial_population(self):
        return [random.sample(range(len(self.points)), len(self.points)) for _ in range(self.population_size)]
    
    def fitness(self, path):
        total_distance = sum(self.distance_matrix[path[i]][path[i+1]] for i in range(len(path)-1))
        total_distance += self.distance_matrix[path[-1]][path[0]]  # back to the starting point
        return 1 / total_distance
    
    def distance(self, point1, point2):
        return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)
    
    def breed(self, parent1, parent2):
        child = [None] * len(parent1)
        start = random.randint(0, len(parent1)-1)
        end = random.randint(start, len(parent1)-1)
        for i in range(start, end+1):
            child[i] = parent1[i]
        remaining = [item for item in parent2 if item not in child]
        for i in range(len(child)):
            if child[i] is None:
                child[i] = remaining.pop(0)
        return child
    
    def mutate(self, path):
        for swapped in range(len(path)):
            if random.random() < self.mutation_rate:
                swap_with = int(random.random() * len(path))
                path[swapped], path[swap_with] = path[swap_with], path[swapped]
        return path
    
    def next_generation(self, population):
        elites = sorted(population, key=lambda x: self.fitness(x), reverse=True)[:self.elite_size]
        children = []
        while len(children) < self.population_size - self.elite_size:
            parent1, parent2 = random.choices(population, weights=[self.fitness(p) for p in population], k=2)
            child = self.breed(parent1, parent2)
            child = self.mutate(child)
            children.append(child)
        return elites + children
    
    def optimize(self):
        population = self.initial_population()
        start_time = time.time()
        for _ in range(self.generations):
            population = self.next_generation(population)
        best_path = max(population, key=lambda x: self.fitness(x))
        min_distance = 1 / self.fitness(best_path)
        
        # Apply 2-opt local search
        best_path = self.local_search_2opt(best_path)
        
        end_time = time.time()
        execution_time = end_time - start_time
        return best_path, min_distance, execution_time
    
    def local_search_2opt(self, path):
        improved = True
        while improved:
            improved = False
            for i, j in combinations(range(1, len(path)), 2):
                new_path = path[:i] + path[i:j+1][::-1] + path[j+1:]
                if self.fitness(new_path) > self.fitness(path):
                    path = new_path
                    improved = True
                    break
        return path
