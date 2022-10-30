from random import randint
from matplotlib import pyplot as plt


def generate_data(number_of_jobs, number_of_products):
    """
    we generate a demo data to simulate our process
    since this problem is to find the best n sequence of job, we coded the chromosome as numbers
    :param number_of_jobs:
    :param number_of_products:
    :return:
    """
    data = dict()
    data['jobs'] = [job for job in range(number_of_jobs)]
    data['process_time'] = [randint(10, 50) for _ in range(number_of_jobs)]
    data['due_time'] = [p+randint(5, 10) for p in data['process_time']]
    data['changeover_time'] = [randint(1, 5) for _ in range(number_of_jobs)]
    data['product_time'] = [randint(0, number_of_products-1) for _ in range(number_of_jobs)]
    return data


def show_generated_data(data):
    """
    We visualize our processes
    :param data:
    :return:
    """
    print('The jobs: ', data['jobs'])
    print('The process time: ', data['process_time'])
    print('The due time: ',  data['due_time'])
    print('The changeOver time: ',  data['changeover_time'])
    print('The product type: ',  data['product_time'])


def show_information(data, jobs):
    print('The jobs: ', jobs)
    print('The process time: ', [data['process_time'][elm] for elm in jobs])
    print('The due time: ',  [data['due_time'][elm] for elm in jobs])
    print('The changeOver time: ',  [data['changeover_time'][elm] for elm in jobs])
    print('The product type: ',   [data['product_time'][elm] for elm in jobs])


def fitness_function_improved(data, jobs):
    """
    Here we computed the Completion time & lateness of the process
    we aim to minimizer this quantity
    we aim to reduce f(S) = sigma(C_i - d_i) where C_i is the total flow time
    :param data:
    :param jobs:
    :return:
    """
    process_time = data['process_time']
    changeover_time = data['changeover_time']
    due_time = data['due_time']
    prorduct_time = data['product_time'] 
    c = 0
    lateness_list = []
    for i in range(0, len(jobs)):
        last_product = prorduct_time[i-1]
        current_product = prorduct_time[i]
        if last_product == current_product:
            c += process_time[jobs[i]]
        elif last_product != current_product:
            c += process_time[jobs[i]] + changeover_time[jobs[i]]
        lateness = c - due_time[jobs[i]]
        if lateness > 0:
            lateness_list.append(lateness)
    return sum(lateness_list)


def fitness_function(data, jobs):
    process_time = data['process_time']
    due_time = data['due_time']

    c = 0
    tardiness_list = []
    for i in range(0, len(jobs)):
        c += process_time[jobs[i]]
        tardiness = c - due_time[jobs[i]]
        if tardiness > 0:
            tardiness_list.append(tardiness)
    return sum(tardiness_list)


def statistics(iteration, populations, scores, data):
    """
    :param iteration:
    :param populations:
    :param scores:
    :param data:
    :return:
    """
    print()
    print(f'Generation: {iteration}, best fitness score: {min(scores)}, low fitness score: {max(scores)}')
    print(f'The mean lateness of the population: {sum(scores)/len(scores)}')
    print(f'Best population: {populations[0]} cost function value: {fitness_function(data, populations[0])}')


def accepted_chromosome(chromosome):
    """
    :param chromosome:
    :return:
    """
    return sorted(list(set(chromosome))) == sorted(chromosome)


def plot_information(generation, error_best_member, mean_error_population, error_worse_population):
    """
    :param generation:
    :param error_best_member:
    :param mean_error_population:
    :param error_worse_population:
    :return:
    """
    fig_evolution_error = plt.figure("Evolution of the lateness of the jobs")
    ax = fig_evolution_error.add_subplot(1, 1, 1)
    ax.plot(range(generation), error_best_member,
            color='tab:blue', label='Error of the best candidates')
    ax.plot(range(generation), mean_error_population,
            color='tab:orange', label='Mean error of the population')
    ax.plot(range(generation), error_worse_population,
            color='tab:red', label='Error of the worst candidate')
    ax.set_xlim([-0.1, generation])
    ax.set_xlabel('Generation')
    ax.set_ylabel('Lateness [h]')
    ax.set_title("Evolution of the lateness")
    ax.grid(True, linestyle='-.')
    ax.legend()
    # display the plot
    plt.show()
