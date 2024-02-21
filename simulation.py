import numpy as np
import random
import matplotlib.pyplot as plt

# User class
class User:
    def __init__(self, id, min_size, job_core_hours):
        self.id = id
        self.min_size = min_size
        self.job_core_hours = job_core_hours

# Resource class
class Resource:
    def __init__(self, id, size, MAX_CORES):
        self.id = id
        self.size = size
        self.MAX_CORES = MAX_CORES
    
    def update_size(self):
        self.size = np.random.randint(1, self.MAX_CORES + 1)

# Cloud platform class
class DATCloudPlatform:
    def __init__(self, users, resources):
        self.users = users
        self.resources = resources
        self.threshold = 0
        self.time_average_revenue = 0
        self.time = 0

    def allocate_resources(self, FIXED_PRICE, ALPHA):
        total_revenue = 0
        user_core_hours_completed = {user.id: 0 for user in self.users}  # Track completed core hours for users

        for user in self.users:
            self.time += 1
            for resource in self.resources:
                resource.update_size()
                # Skip if user has completed their required core hours
                if user_core_hours_completed[user.id] >= user.job_core_hours:
                    continue
                
                charge = self.calculate_charge(user, resource, FIXED_PRICE, ALPHA)
                if charge >= self.threshold and resource.size >= user.min_size:
                    # Calculate the actual core hours that can be allocated
                    allocatable_core_hours = min(resource.size, user.job_core_hours - user_core_hours_completed[user.id])
                    total_revenue += charge * allocatable_core_hours
                    user_core_hours_completed[user.id] += allocatable_core_hours
                    self.update_time_average_revenue(charge * allocatable_core_hours)
                    break
            else:
                # Update revenue without adding new revenue if no resource is allocated
                self.update_time_average_revenue(0)

        return total_revenue

    def calculate_charge(self, user, resource, FIXED_PRICE, ALPHA):
        return FIXED_PRICE * user.min_size + ALPHA * (resource.size - user.min_size)

    def update_time_average_revenue(self, revenue):
        self.time_average_revenue = (self.time_average_revenue * (self.time - 1) + revenue) / self.time
        self.threshold = BETA * self.time_average_revenue

class Simulator:
    def __init__(self):
        self.MAX_CORES = 10  # Maximum number of cores in a harvesting resource
        self.FIXED_PRICE = 0.1  # Fixed price per core hour
        self.ALPHA = 0.3        # Discount ratio for additional resources

    # Function for DAT algorithm simulation
    def simulate_dat_algorithm(self, users, resources):
        platform = DATCloudPlatform(users, resources)
        return platform.allocate_resources(self.FIXED_PRICE, self.ALPHA)
    
    # Calculate VCG price
    def update_fixed_price(self):
        # Calculate the total revenue with all users
        total_value_with_all = self.calculate_offline_optimal_revenue(self.users, self.resources)

        vcg_payments = []
        for user in self.users:
            # Temporarily exclude the current user from the list
            users_without_current = [u for u in self.users if u.id != user.id]

            # Calculate the total revenue without the current user
            total_value_without_user = self.calculate_offline_optimal_revenue(users_without_current, self.resources)

            # The VCG payment for the current user is the difference in total value
            vcg_payment = total_value_with_all - total_value_without_user
            vcg_payments.append(vcg_payment)

        # Update FIXED_PRICE based on the VCG payments
        if vcg_payments:  # Ensure the list is not empty to avoid division by zero
            self.FIXED_PRICE = sum(vcg_payments)* BETA
        else:
            self.FIXED_PRICE = 0  # Or some default value if no users exist
        return self.FIXED_PRICE

    # Function for random allocation simulation
    def simulate_random_allocation(self, users, resources):
        total_revenue = 0
        for user in users:
            chosen_resource = random.choice(resources)
            chosen_resource.update_size()  # Simulate dynamic resource size change
            if chosen_resource.size >= user.min_size:
                charge = self.FIXED_PRICE * user.min_size + self.ALPHA * (chosen_resource.size - user.min_size)
                total_revenue += charge
        return total_revenue

    # Function to simulate Greedy Minimum Resource Matching (GMRM)
    def greedy_minimum_resource_matching(self, users, resources):
        total_revenue = 0
        for user in users:
            # Sort resources by size that meets the user requirement
            suitable_resources = sorted((res for res in resources if res.size >= user.min_size), key=lambda x: x.size)
            if suitable_resources:
                chosen_resource = suitable_resources[0]
                charge = self.FIXED_PRICE * user.min_size + self.ALPHA * (chosen_resource.size - user.min_size)
                total_revenue += charge
        return total_revenue

    # Function for offline optimal revenue calculation
    def calculate_offline_optimal_revenue(self, users, resources):
        total_revenue = 0
        for user in users:
            max_revenue_for_user = 0
            for resource in resources:
                resource.update_size()  # Simulate dynamic resource size change
                if resource.size >= user.min_size:
                    charge = self.FIXED_PRICE * user.min_size + self.ALPHA * (resource.size - user.min_size)
                    max_revenue_for_user = max(max_revenue_for_user, charge)
            total_revenue += max_revenue_for_user
        return total_revenue

    # Function to simulate Maximum Resource Matching (MRM)
    def maximum_resource_matching(self, users, resources):
        total_revenue = 0
        for user in users:
            suitable_resources = sorted((res for res in resources if res.size >= user.min_size), key=lambda x: x.size, reverse=True)
            if suitable_resources:
                chosen_resource = suitable_resources[0]
                charge = self.FIXED_PRICE * user.min_size + self.ALPHA * (chosen_resource.size - user.min_size)
                total_revenue += charge
        return total_revenue

    # Generate plots for different distributions
    def generate_plots(self, distributions, beta_values, revenue_functions, function_names):
        for dist_name, dist_func in distributions.items():
            users, resources = dist_func()
            plt.figure(figsize=(12, 7))
            for rev_func, func_name in zip(revenue_functions, function_names):
                revenues = []
                for beta in beta_values:
                    global BETA
                    BETA = beta
                    revenues.append(rev_func(users, resources))
                plt.plot(beta_values, revenues, label=func_name)
            
            plt.title(f'Platform Revenue Comparison for {dist_name}')
            plt.xlabel('Beta')
            plt.ylabel('Total Platform Revenue')
            plt.legend()
            plt.grid(True)
            plt.savefig(f'platform_revenue_{dist_name}.png')
            plt.close()

    # Helper function to generate users
    def generate_users(self, num_users, max_cores):
        return [User(i, np.random.randint(1, max_cores // 2), np.random.randint(10, 100)) for i in range(num_users)]

    # Helper function to generate resources with high variability in size
    def high_variability_resources(self, num_resources, max_cores):
        return [Resource(j, np.random.randint(1, max_cores + 1), max_cores) for j in range(num_resources)]

    # Helper function to generate resources with uniform high demand size
    def uniform_high_demand_resources(self, num_resources, max_cores):
        uniform_size = max_cores  # All resources have the maximum size
        return [Resource(j, uniform_size, max_cores) for j in range(num_resources)]

    # Helper function to generate resources with gradual increase in size
    def gradual_increase_resources(self, num_resources, max_cores):
        return [Resource(j, min(j + 1, max_cores), max_cores) for j in range(num_resources)]

    # Helper function to generate resources with random size
    def random_resources(self, num_resources, max_cores):
        return [Resource(j, np.random.randint(1, max_cores + 1), max_cores) for j in range(num_resources)]

