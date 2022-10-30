import random
from utils import generate_data, show_generated_data, fitness_function, show_information, plot_information  
from GeneticAlgorithm import genetic_evolution


random.seed(0)
# generations
generations = 1000
# top population
top = 10
# population size
population_size = 5000
# number of tasks
nb_task = 18
# number of product
nb_product = 5
# generate data
data = generate_data(nb_task, nb_product)
# jobs sequence
jobs = data['jobs']

show_generated_data(data)
print(f'total flow time {fitness_function(data, jobs)} Hour')
best_pop, mean_error_population, error_best_population, error_worst_population = genetic_evolution(data=data, subset=top,
                                                                                         verbosity=False,
                                                                                         population_size=population_size,
                                                                                         generations=generations)

plot_information(generations, mean_error_population, error_best_population, error_worst_population)


print("_"*50)
show_information(data, best_pop)
print(f'total flow time {fitness_function(data, best_pop)} Hour')
