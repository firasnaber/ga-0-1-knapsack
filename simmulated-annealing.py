import random
import math

def knapsack_value(solution, values, weights, capacity):
    total_value = sum(v for v, s in zip(values, solution) if s)
    total_weight = sum(w for w, s in zip(weights, solution) if s)
    if total_weight > capacity:
        return 0  # invalid solution if overweight
    return total_value

def perturb(solution):
    new_solution = solution.copy()
    idx = random.randint(0, len(solution) - 1)
    new_solution[idx] = 1 - new_solution[idx]  # flip item inclusion
    return new_solution

def simulated_annealing(values, weights, capacity, initial_temp, alpha, beta, i0, max_iterations):
    S = [random.randint(0, 1) for _ in values]  # initial random solution
    T = initial_temp
    iterations = i0
    best_solution = S[:]
    best_value = knapsack_value(S, values, weights, capacity)
    
    total_outer = 0

    while total_outer < max_iterations:
        print(f"Iteration {total_outer + 1}, Temperature: {T:.4f}, Best Value: {best_value}")
        for _ in range(iterations):
            NewS = perturb(S)
            h_S = -knapsack_value(S, values, weights, capacity)
            h_NewS = -knapsack_value(NewS, values, weights, capacity)
            if h_NewS < h_S or random.random() < math.exp((h_S - h_NewS) / T):
                S = NewS
                current_value = knapsack_value(S, values, weights, capacity)
                if current_value > best_value:
                    best_solution = S[:]
                    best_value = current_value
        T = alpha * T
        iterations = int(beta * iterations) if beta * iterations >= 1 else 1  # ensure at least 1 iteration
        total_outer += 1

    return best_solution, best_value

# Example usage
if __name__ == "__main__":
    values = [40, 50, 40, 45, 40, 30, 40, 20, 30, 40, 50, 40, 45, 40, 42]
    weights = [10, 10, 15, 15, 16, 25, 20, 15, 18, 22, 11, 16, 16, 11, 15]
    capacity = 50

    best_sol, best_val = simulated_annealing(
        values, weights, capacity,
        initial_temp=1000, alpha=0.98, beta=1.02, i0=1000, max_iterations=100
    )

    print("\nFinal Best Solution:", best_sol)
    print("Final Best Value:", best_val)
