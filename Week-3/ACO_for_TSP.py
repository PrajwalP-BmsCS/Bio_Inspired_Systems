import numpy as np
import random
import matplotlib.pyplot as plt

class AntColonyOptimizer:
    def __init__(self, cities, num_ants=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, iterations=100):
       
        self.cities = np.array(cities)
        self.num_cities = len(cities)
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.iterations = iterations

        # Initialize pheromone levels and heuristic values
        self.pheromone = np.ones((self.num_cities, self.num_cities)) / self.num_cities
        self.heuristic = self._calculate_heuristic()

    def _calculate_heuristic(self):
        """
        Calculate the heuristic values based on distances between cities.
        """
        distances = np.linalg.norm(self.cities[:, np.newaxis] - self.cities[np.newaxis, :], axis=-1)
        return 1 / (distances + np.eye(self.num_cities))  # Avoid division by zero

    def _select_next_city(self, current_city, visited):
        """
        Select the next city for the ant to visit based on pheromone and heuristic information.
        """
        pheromone = self.pheromone[current_city]
        heuristic = self.heuristic[current_city]

        probabilities = (pheromone ** self.alpha) * (heuristic ** self.beta)
        probabilities[visited] = 0  # Set probability to 0 for visited cities
        probabilities /= probabilities.sum()  # Normalize probabilities

        return np.random.choice(np.arange(self.num_cities), p=probabilities)

    def _update_pheromones(self, all_routes, all_lengths):
        """
        Update pheromone levels based on the routes taken by ants.
        """
        self.pheromone *= (1 - self.evaporation_rate)  # Evaporate pheromones

        for i in range(self.num_ants):
            for j in range(self.num_cities):
                self.pheromone[all_routes[i][j], all_routes[i][(j + 1) % self.num_cities]] += 1 / all_lengths[i]

    def solve(self):
        """
        Execute the Ant Colony Optimization algorithm to find the best route.

        Returns:
            best_route: The best route found.
            best_length: The length of the best route found.
            best_routes_history: History of the best routes in each iteration.
        """
        best_route = None
        best_length = float('inf')
        best_routes_history = []

        for iteration in range(self.iterations):
            all_routes = []
            all_lengths = []

            for ant in range(self.num_ants):
                visited = np.zeros(self.num_cities, dtype=bool)
                current_city = random.randint(0, self.num_cities - 1)
                route = [current_city]
                visited[current_city] = True

                for _ in range(self.num_cities - 1):
                    next_city = self._select_next_city(current_city, visited)
                    route.append(next_city)
                    visited[next_city] = True
                    current_city = next_city

                # Complete the cycle back to the starting city
                route.append(route[0])
                length = sum(np.linalg.norm(self.cities[route[i]] - self.cities[route[i + 1]]) for i in range(self.num_cities))

                all_routes.append(route)
                all_lengths.append(length)

                # Update the best solution found
                if length < best_length:
                    best_length = length
                    best_route = route

            # Print the best length found in this iteration
            print(f"Iteration {iteration + 1}: Best Length = {best_length:.2f}")

            # Store the best route found in this iteration
            best_routes_history.append((iteration, best_route, best_length))

            # Update pheromones
            self._update_pheromones(all_routes, all_lengths)

        return best_route, best_length, best_routes_history

    def plot_route(self, route, iteration, length):
        """
        Plot a single route.

        Parameters:
            route: The route to plot.
            iteration: The iteration number.
            length: The length of the route.
        """
        plt.figure(figsize=(8, 6))
        x = self.cities[route, 0]
        y = self.cities[route, 1]
        plt.plot(x, y, 'r-', linewidth=2)

        plt.scatter(self.cities[:, 0], self.cities[:, 1], s=100, c='blue', marker='o', label='Cities')  # Plot cities
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        plt.title(f"Ant Colony Optimization Route - Iteration {iteration + 1}")
        plt.grid(True)
        plt.legend()
        plt.show()

# Example usage
if __name__ == "__main__":
    num_points = 200  # Adjust for performance; fewer points is faster
    x_range = (0, 1000)  # Adjust as needed
    y_range = (0, 1000)

    cities = [(random.uniform(*x_range), random.uniform(*y_range)) for _ in range(num_points)]
    aco = AntColonyOptimizer(cities)
    best_route, best_length, best_routes_history = aco.solve()
    
    print("Best Route:", best_route)
    print("Best Length:", best_length)

    # Plot selected iterations (1st, 25th, 50th, 100th), excluding 75th
    selected_iterations = [0, 24, 49, 99]  
    for iteration in selected_iterations:
        _, route, length = best_routes_history[iteration]
        aco.plot_route(route, iteration, length)
