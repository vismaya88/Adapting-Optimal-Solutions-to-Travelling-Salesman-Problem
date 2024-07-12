import os
from gen import GeneticAlgorithmTSP
from hyb import tsp_hybrid
from si import simulated_annealing
from twoopt import tsp_2opt
from nn import tsp_nearest_neighbor
from matplotlib import pyplot as plt

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

# Function to visualize the path
def visualize_path(points, path):
    x = [points[i][0] for i in path] + [points[path[0]][0]]
    y = [points[i][1] for i in path] + [points[path[0]][1]]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    
    for i, point in enumerate(path):
        plt.text(points[point][0], points[point][1], str(i+1), fontsize=9, ha='right')
    
    plt.title('TSP Path Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.show()

# Main function
def main():
    folder = "datasets"
    datasets = list_datasets(folder)
    
    print("Available datasets:")
    for i, dataset in enumerate(datasets):
        print(f"{i + 1}. {dataset}")

    choice = int(input("Enter the number associated with the dataset you wish to choose: ")) - 1

    if 0 <= choice < len(datasets):
        selected_file = datasets[choice]
        points = read_dataset(os.path.join(folder, selected_file))

        if len(points) == 0:
            print("The selected dataset is empty or contains no valid data points.")
            return
        
        print("Dataset loaded successfully.")
        print("Number of points in the dataset:", len(points))

        results = {}

        # Using Genetic Algorithm
        print("\nRunning Genetic Algorithm...")
        tsp_solver = GeneticAlgorithmTSP(points)
        best_path_genetic, min_distance_genetic, execution_time_genetic = tsp_solver.optimize()
        results['Genetic Algorithm'] = (best_path_genetic, min_distance_genetic, execution_time_genetic)

        print("\nGenetic algorithm:")
        print("Shortest Path:", best_path_genetic)
        print("Shortest Distance:", min_distance_genetic)
        print("Execution Time:", execution_time_genetic, "seconds")

        # Using Hybrid Algorithm
        print("\nRunning Hybrid Algorithm...")
        best_path_hybrid, min_distance_hybrid, execution_time_hybrid = tsp_hybrid(points)
        results['Hybrid Algorithm'] = (best_path_hybrid, min_distance_hybrid, execution_time_hybrid)

        print("\nHybrid algorithm:")
        print("Shortest Path:", best_path_hybrid)
        print("Shortest Distance:", min_distance_hybrid)
        print("Execution Time:", execution_time_hybrid, "seconds")

        # Using Simulated Annealing Algorithm
        print("\nRunning Simulated Annealing Algorithm...")
        best_path_annealing, min_distance_annealing, execution_time_annealing = simulated_annealing(points)
        results['Simulated Annealing'] = (best_path_annealing, min_distance_annealing, execution_time_annealing)

        print("\nSimulated Annealing algorithm:")
        print("Shortest Path:", best_path_annealing)
        print("Shortest Distance:", min_distance_annealing)
        print("Execution Time:", execution_time_annealing, "seconds")

        # Using 2-opt Algorithm
        print("\nRunning 2-opt Algorithm...")
        best_path_2opt, min_distance_2opt, execution_time_2opt = tsp_2opt(points, list(range(len(points))))
        results['2-opt Algorithm'] = (best_path_2opt, min_distance_2opt, execution_time_2opt)

        print("\n2-opt algorithm:")
        print("Shortest Path:", best_path_2opt)
        print("Shortest Distance:", min_distance_2opt)
        print("Execution Time:", execution_time_2opt, "seconds")

        # Using Nearest Neighbor Algorithm
        print("\nRunning Nearest Neighbor Algorithm...")
        shortest_path_nearest_neighbor, min_distance_nearest_neighbor, execution_time_nearest_neighbor = tsp_nearest_neighbor(points)
        results['Nearest Neighbor'] = (shortest_path_nearest_neighbor, min_distance_nearest_neighbor, execution_time_nearest_neighbor)

        print("\nNearest Neighbor heuristic")
        print("Shortest Path:", shortest_path_nearest_neighbor)
        print("Shortest Distance:", min_distance_nearest_neighbor)
        print("Execution Time:", execution_time_nearest_neighbor, "seconds")

        # Visualizing paths
        visualize_path(points, best_path_genetic)
        visualize_path(points, best_path_hybrid)
        visualize_path(points, best_path_annealing)
        visualize_path(points, best_path_2opt)
        visualize_path(points, shortest_path_nearest_neighbor)

        # Finding the best method according to execution time and total distance
        best_by_distance = min(results.items(), key=lambda x: x[1][1])
        best_by_time = min(results.items(), key=lambda x: x[1][2])

        print("\nBest Method by Total Distance:")
        print(f"{best_by_distance[0]} with distance {best_by_distance[1][1]}")

        print("\nBest Method by Execution Time:")
        print(f"{best_by_time[0]} with execution time {best_by_time[1][2]} seconds")

        # Determine the overall best method based on combined rank
        sorted_by_distance = sorted(results.items(), key=lambda x: x[1][1])
        sorted_by_time = sorted(results.items(), key=lambda x: x[1][2])

        overall_ranks = {name: 0 for name in results}
        
        for rank, (name, _) in enumerate(sorted_by_distance):
            overall_ranks[name] += rank
        for rank, (name, _) in enumerate(sorted_by_time):
            overall_ranks[name] += rank

        overall_best = min(overall_ranks.items(), key=lambda x: x[1])

        print("\nOverall Best Method:")
        print(f"{overall_best[0]} with combined rank {overall_best[1]}")
        
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
