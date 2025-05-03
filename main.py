from random import choice, choices, randint, random, sample, shuffle
from sys import exit


def init_population(weights: list[int], n_samples: int) -> list[list[int]]:
    population = []
    while len(population) < N_SAMPLES:
        individual = [randint(0, 1) for _ in range(len(WEIGHTS))]
        if any(individual):
            population.append(individual)
    
    return population

def fitness(population: list[list[int]]) -> list[int]:
    fitness_scores = []
    weights_list = []
    min_fitness = float("inf")
    max_fitness = 0
    
    for chromosome in population:
        total_val = 0
        total_weight = 0
        for i, gene in enumerate(chromosome):
            if gene == 1:
                total_val += VALUES[i]
                total_weight += WEIGHTS[i]

        fitness_scores.append(total_val)
        weights_list.append(total_weight)
        
        if total_weight <= CAPACITY:
            min_fitness = min(min_fitness, total_val) # find min feasible fitness without a separate loop
            max_fitness = max(max_fitness, total_val) # find max feasible fitness without separate loop

    min_max_avg = (min_fitness + max_fitness) // 2

    # Handling infeasibles
    for i in range(len(fitness_scores)):
        if weights_list[i] > CAPACITY:
            over_cap = weights_list[i] - CAPACITY
            new_fitness = max(0, min_max_avg - over_cap)
            fitness_scores[i] = new_fitness
    
    return fitness_scores

def elitism(old_pop, old_fit, new_pop, n_elites=1):
    # Ensure n_elites doesn't exceed population size
    n_elites = min(n_elites, len(old_pop))

    # Find indices of the top n_elites in the old population
    sorted_indices = sorted(range(len(old_fit)), key=lambda x: old_fit[x], reverse=True)
    elites = [old_pop[i] for i in sorted_indices[:n_elites]]

    # Find indices of the worst n_elites in the new population (lowest fitness)
    new_fit = fitness(new_pop)
    worst_indices = sorted(range(len(new_fit)), key=lambda x: new_fit[x])[:n_elites]  # Ensure it's the worst

    # Replace worst individuals with elites
    for i in range(n_elites):
        new_pop[worst_indices[i]] = elites[i]

    return new_pop

def selection(population, fitness_scores, method="tournament", k=0.75) -> list[list[int]]:
    if method == "tournament":
        selected = []
        for _ in range(len(population)):
            rand_indexes = sample(range(len(population)), 2)
            fitness_1 = fitness_scores[rand_indexes[0]]
            fitness_2 = fitness_scores[rand_indexes[1]]
            r = random()
            if r < k:
                if fitness_1 >= fitness_2:
                    parent = population[rand_indexes[0]]
                else:
                    parent = population[rand_indexes[1]]
            else:
                if fitness_1 >= fitness_2:
                    parent = population[rand_indexes[1]]
                else:
                    parent = population[rand_indexes[0]]
            selected.append(parent)
    elif method == "roulette":
        fitness_total = sum(fitness_scores)
        odds = []
        for score in fitness_scores:
            odds.append(score / fitness_total)
        selected = choices(population, odds, k=len(population))
    else:
        exit("Error: \"method\" argument only accepts \"tournament\" or \"roulette\".")
    return selected

def crossover(parents: list[list[int]], method: str = "single") -> list[list[int]]:
    children = []
    shuffle(parents)  # Randomize the order once

    for i in range(0, len(parents), 2):  # Pair parents sequentially
        parent_1 = parents[i]
        
        # Make sure if the number of parents is odd, handle the last one
        if i + 1 < len(parents):
            parent_2 = parents[i + 1]
        else:
            parent_2 = choice(parents)
        
        if method == "single":
            crosspoint = randint(1, len(parent_1) - 1)
            child_1 = parent_1[:crosspoint] + parent_2[crosspoint:]
            child_2 = parent_2[:crosspoint] + parent_1[crosspoint:]
            children.append(child_1)
            children.append(child_2)
        
        elif method == "multi":
            crosspoints = sorted(sample(range(1, len(parent_1)), 2))  # Ensure points are distinct and sorted
            child_1 = parent_1[:crosspoints[0]] + parent_2[crosspoints[0]:crosspoints[1]] + parent_1[crosspoints[1]:]
            child_2 = parent_2[:crosspoints[0]] + parent_1[crosspoints[0]:crosspoints[1]] + parent_2[crosspoints[1]:]
            children.append(child_1)
            children.append(child_2)
        
        else:
            exit("Error: \"method\" argument only accepts \"single\" or \"multi\".")

    return children

def mutation(generation, method="flip", prob=0.02):
    if method == "flip":
        for chromosome in generation:
            r = random()
            if r <= prob:
                rand_index = randint(0, len(chromosome) - 1)
                chromosome[rand_index] ^= 1  # Flip bit (0 -> 1 or 1 -> 0)
    elif method == "swap":
        for chromosome in generation:
            r = random()
            if r <= prob:
                i, j = sample(range(len(chromosome)), 2)
                chromosome[i], chromosome[j] = chromosome[j], chromosome[i]  # Swap two bits
    else:
        exit("Error: \"method\" argument only accepts \"flip\" or \"swap\".")
    return generation


if __name__ == "__main__":
    WEIGHTS = [10, 10, 15, 15, 16, 25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
    VALUES = [40, 50, 40, 45, 40, 30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
    CAPACITY = 50
    TOTAL = sum(VALUES)

    # Settings
    N_SAMPLES = 400
    N_GENERATIONS = 100
    SELECTION_METHOD = "tournament"  # or "roulette"
    CROSSOVER_METHOD = "single"      # or "multi"
    MUTATION_METHOD = "flip"          # or "swap"
    MUTATION_PROB = 0.02

    # Initialize population
    while True:
        pop = init_population(WEIGHTS, N_SAMPLES)
        fit = fitness(pop)
        if any(score > 0 for score in fit):
            break

    # Evolution loop
    for generation in range(N_GENERATIONS):
        fit = fitness(pop)

        selected = selection(pop, fit, method=SELECTION_METHOD)
        children = crossover(selected, method=CROSSOVER_METHOD)
        mutated = mutation(children, method=MUTATION_METHOD, prob=MUTATION_PROB)

        # Apply elitism
        pop = elitism(pop, fit, mutated, n_elites=1)

        # Print progress
        best_fit = max(fitness(pop))
        print(f"Generation {generation+1}: Best Fitness = {best_fit}")

    # After evolution
    final_fitness = fitness(pop)
    best_solution = pop[final_fitness.index(max(final_fitness))]
    print("\nBest solution found:", best_solution)
    print("Fitness of best solution:", max(final_fitness))