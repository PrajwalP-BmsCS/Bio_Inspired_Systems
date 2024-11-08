import numpy as np
import math

def objective_function(x):
    return np.sum(x**2)

def initialize_nests(num_nests, num_dimensions):
    return np.random.uniform(-5, 5, (num_nests, num_dimensions))

def levy_flight(solutions, beta=1.5):
    sigma = (math.gamma(1 + beta) * np.sin(np.pi * beta / 2) / 
             (math.gamma((1 + beta) / 2) * beta * np.power(2, (beta - 1) / 2)))**(1 / beta)
    s = np.random.normal(0, sigma, size=solutions.shape)
    return solutions + 0.01 * s

def evaluate_fitness(nests):
    fitness = np.apply_along_axis(objective_function, 1, nests)
    return fitness

def cuckoo_search(num_nests, num_dimensions, max_iterations, Pa):
    nests = initialize_nests(num_nests, num_dimensions)
    fitness = evaluate_fitness(nests)
    best_nest = nests[np.argmin(fitness)]
    best_fitness = np.min(fitness)
    
    for iteration in range(max_iterations):
        new_nests = levy_flight(nests)
        new_fitness = evaluate_fitness(new_nests)
        better_nests_idx = new_fitness < fitness
        nests[better_nests_idx] = new_nests[better_nests_idx]
        fitness[better_nests_idx] = new_fitness[better_nests_idx]
        
        num_replace = int(Pa * num_nests)
        worst_nests_idx = np.argsort(fitness)[-num_replace:]
        nests[worst_nests_idx] = initialize_nests(num_replace, num_dimensions)
        fitness[worst_nests_idx] = evaluate_fitness(nests[worst_nests_idx])
        
        current_best_fitness = np.min(fitness)
        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_nest = nests[np.argmin(fitness)]
        
        print(f"Iteration {iteration + 1}/{max_iterations} - Best Fitness: {best_fitness}")
    
    return best_nest, best_fitness

best_solution, best_fitness = cuckoo_search(num_nests, num_dimensions, max_iterations, Pa)

print("\nBest solution found:", best_solution)
print("Best fitness value:", best_fitness)
