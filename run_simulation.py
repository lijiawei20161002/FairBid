import numpy as np
import random
import matplotlib.pyplot as plt
from simulation import Simulator

# Constants
NUM_USERS = 100   # Total number of users
NUM_RESOURCES = 50  # Total number of harvesting resources
BETA = 0.5         # Algorithm parameter

simulator = Simulator()
# Define different scenarios
distributions = {
    'High Variability': lambda: (simulator.generate_users(NUM_USERS, simulator.MAX_CORES), simulator.high_variability_resources(NUM_RESOURCES, simulator.MAX_CORES)),
    'Uniform High Demand': lambda: (simulator.generate_users(NUM_USERS, simulator.MAX_CORES), simulator.uniform_high_demand_resources(NUM_RESOURCES, simulator.MAX_CORES)),
    'Gradual Increase': lambda: (simulator.generate_users(NUM_USERS, simulator.MAX_CORES), simulator.gradual_increase_resources(NUM_RESOURCES, simulator.MAX_CORES)),
    'Random': lambda: (simulator.generate_users(NUM_USERS, simulator.MAX_CORES), simulator.random_resources(NUM_RESOURCES, simulator.MAX_CORES))
}

# Beta values from 0.1 to 1.0 for simulation
beta_values = np.linspace(0.1, 1.0, 10)

# List of revenue functions and their names for plotting
revenue_functions = [simulator.simulate_dat_algorithm, simulator.simulate_random_allocation, simulator.calculate_offline_optimal_revenue, simulator.greedy_minimum_resource_matching]
function_names = ['DAT Algorithm', 'Random Allocation', 'Offline Optimal', 'GMRM']

# Generate the plots
simulator.generate_plots(distributions, beta_values, revenue_functions, function_names)