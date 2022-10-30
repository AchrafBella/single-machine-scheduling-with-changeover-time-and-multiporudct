import random as random
from math import factorial
from numpy.random import permutation
from utils import fitness_function, statistics, fitness_function_improved
import numpy as np


def generate_population(data, population_size):
    """
        To generate all the possible combination, for n Jobs & m Machine we have (n!)^m
    :param data:
    :param population_size:
    :return:
    """
    max_permutation = factorial(max(data['jobs']))
    assert max_permutation >= population_size
    return [list(permutation(len(data['jobs']))) for _ in range(population_size)]


def evaluate_fitness(data, population):
    """
    :param data:
    :param population:
    :return:
    """
    return [(chromosome, fitness_function_improved(data, chromosome)) for chromosome in list(population)]


def natural_selection(population):
    """
    :param population:
    :return:
    """
    sorted_population = sorted(population, key=lambda x: x[1], reverse=False)
    population = [couple[0] for couple in sorted_population]
    fitness_scores = [couple[1] for couple in sorted_population]
    return population, fitness_scores


def crossover1(population, subset):
    # subset of the fittest population
    top_population = population[:subset]
    # select the 2 parents
    parents = random.sample(top_population, 2)
    # turn the parent into chromosomes
    chromosome1, chromosome2 = parents[0], parents[1]
    cross_point = random.randint(1, len(chromosome1)-1)
    offsprings1 = chromosome1[:cross_point]+sorted(chromosome1[cross_point:])
    offsprings2 = chromosome2[:cross_point]+sorted(chromosome2[cross_point:], reverse=True)
    population.pop(-1)
    population.pop(-1)
    population.extend([offsprings2, offsprings1])
    return population


def crossover2(population, subset):
    # subset of the fittest population
    top_population = population[:subset]
    # select the 2 parents
    parents = random.sample(top_population, 2)
    # turn the parent into chromosomes
    chromosome1, chromosome2 = parents[0], parents[1]
    cross_point1 = random.randint(0, len(chromosome1) - int(len(chromosome1)//2))
    cross_point2 = random.randint(int(len(chromosome1)//2)+1, len(chromosome1))

    offsprings1 = chromosome1[:cross_point1] + ['' for _ in range(cross_point1, cross_point2)] + chromosome1[
                                                                                                 cross_point2:]
    offsprings2 = chromosome2[:cross_point1] + ['' for _ in range(cross_point1, cross_point2)] + chromosome2[
                                                                                                 cross_point2:]

    for gene in reversed(chromosome2):
        if gene not in offsprings1 and gene != '':
            i = cross_point1
            offsprings1.insert(i, gene)
            offsprings1.remove('')
            i += 1

    for gene in reversed(chromosome1):
        if gene not in offsprings2:
            i = cross_point1
            offsprings2.insert(i, gene)
            offsprings2.remove('')
            i += 1

    population.pop(-1)
    population.pop(-1)
    population.extend([offsprings2, offsprings1])
    return population


def mutation1(population):
    chromosome = random.choice(population)
    population.remove(chromosome)
    mutated_chromosome = random.sample(chromosome, len(chromosome))
    population.append(mutated_chromosome)
    return population


def mutation2(population):
    chromosome = random.choice(population)
    population.remove(chromosome)

    random_job1 = random.randint(0, len(chromosome)-1)
    random_job2 = random.randint(0, len(chromosome)-1)

    i, j = chromosome.index(random_job1), chromosome.index(random_job2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]

    population.append(chromosome)
    return population


def mutation3(population):
    p_mut = 0.4
    if p_mut < np.random():
        for chromosome in population:
            random_job1 = random.randint(0, len(chromosome)-1)
            random_job2 = random.randint(0, len(chromosome)-1)
            i, j = chromosome.index(random_job1), chromosome.index(random_job2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return population


def genetic_evolution(data, subset, verbosity, generations=100, population_size=100):
    """
    :param data:
    :param subset:
    :param verbosity:
    :param generations:
    :param population_size:
    :return: 3 list of the information correct through the generation
    """
    mean_error_population = []
    error_best_population = []
    error_worst_population = []
    i = 0
    population = generate_population(data, population_size)
    while i < generations:
        fitness = evaluate_fitness(data, population)
        population, fitness_scores = natural_selection(fitness)

        if verbosity:
            statistics(i, population, fitness_scores, data)

        population = crossover2(population, subset)
        population = mutation1(population)

        mean_error_population.append(np.mean(fitness_scores))
        error_best_population.append(fitness_scores[0])
        error_worst_population.append(fitness_scores[-1])

        i += 1
    
    return population[-1], mean_error_population, error_best_population, error_worst_population
