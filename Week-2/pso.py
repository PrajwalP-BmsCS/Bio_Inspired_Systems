import random, math, sys

def fitness_rastrigin(position):
    return sum(x**2 - 10 * math.cos(2 * math.pi * x) + 10 for x in position)

def fitness_sphere(position):
    return sum(x**2 for x in position)

class Particle:
    def __init__(self, fitness, dim, minx, maxx, seed):
        rnd = random.Random(seed)
        self.position = [rnd.uniform(minx, maxx) for _ in range(dim)]
        self.velocity = [rnd.uniform(minx, maxx) for _ in range(dim)]
        self.fitness = fitness(self.position)
        self.best_pos = self.position[:]

def pso(fitness, max_iter, num_particles, dim, minx, maxx):
    w, c1, c2 = 0.729, 1.49445, 1.49445
    rnd = random.Random(0)
    swarm = [Particle(fitness, dim, minx, maxx, i) for i in range(num_particles)]
    global_best_pos = min(swarm, key=lambda p: p.fitness).position

    for _ in range(max_iter):
        for p in swarm:
            for i in range(dim):
                r1, r2 = rnd.random(), rnd.random()
                p.velocity[i] = w * p.velocity[i] + c1 * r1 * (p.best_pos[i] - p.position[i]) + c2 * r2 * (global_best_pos[i] - p.position[i])
                p.position[i] = max(minx, min(maxx, p.position[i] + p.velocity[i]))
            p.fitness = fitness(p.position)
            if p.fitness < fitness(p.best_pos):
                p.best_pos = p.position[:]
        global_best_pos = min(swarm, key=lambda p: p.fitness).position

    return global_best_pos

def run_pso(fitness_func, func_name, dim=3, num_particles=50, max_iter=100):
    print(f"\nRunning PSO on {func_name}, dim={dim}, particles={num_particles}, iter={max_iter}")
    best_pos = pso(fitness_func, max_iter, num_particles, dim, -10.0, 10.0)
    print(f"Best solution: {['%.6f' % x for x in best_pos]}, Fitness: {fitness_func(best_pos):.6f}")

# Run for both functions
run_pso(fitness_rastrigin, "Rastrigin")
run_pso(fitness_sphere, "Sphere")
