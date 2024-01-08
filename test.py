import numpy as np
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import numpy as np

# Placeholder data for demonstration purposes
beta_values = np.linspace(0.1, 1.0, 10)
revenue_our_algorithm = [160, 165, 170, 175, 180, 185, 190, 195, 200, 205]  # This line represents our algorithm's revenue

# Since random and greedy allocations are not affected by beta, they will be constant lines
random_allocation_revenue = [130] * len(beta_values)  # Constant revenue for random allocation
greedy_allocation_revenue = [180] * len(beta_values)  # Constant revenue for greedy allocation

# Create a new figure
plt.rcParams.update({'font.size': 20})
plt.figure(figsize=(12, 7))

# Plot the data with markers for our algorithm
plt.plot(beta_values, revenue_our_algorithm, marker='o', label='Our Algorithm', linestyle='-')

# Plot horizontal lines for random and greedy allocations
plt.axhline(y=random_allocation_revenue[0], label='Random Allocation', color='green', linestyle='--')
plt.axhline(y=greedy_allocation_revenue[0], label='Greedy Allocation', color='purple', linestyle='--')

# Add title and labels
plt.title('Platform Revenue Comparison')
plt.xlabel('Beta')
plt.ylabel('Total Platform Revenue')

# Legend
plt.grid()
plt.legend()
plt.plot()

# Save the figure to a file
plt.savefig('allocation_revenue_varying_alpha.png')
