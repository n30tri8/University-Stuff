import Chromosome
import plot
import numpy
import random

Mu = 10
Lambda = 1*Mu
crossover_probability = 0.4


def generate_initial_population():
    list_of_chromosomes = []
    for i in range(Mu+Lambda):
        list_of_chromosomes.append(Chromosome.Chromosome())
    return list_of_chromosomes

def generate_new_seed(population): # selection
    """
    :return: return lambda selected parents
    """
    choices = {tuple(chromosome.genes): chromosome.score for chromosome in population}

    fitness = choices.values()
    total_fit = float(sum(fitness))
    relative_fitness = [f/total_fit for f in fitness]
    probabilities = [sum(relative_fitness[:i+1]) 
                     for i in range(len(relative_fitness))]

    chosen = []
    for n in range(Lambda):
        r = random.random()
        for (i, individual) in enumerate(population):
            if r <= probabilities[i]:
                copied_individual = Chromosome.Chromosome(individual.genes.copy())
                chosen.append(copied_individual)
                break

    return chosen

def crossover(chromosome1, chromosome2):
    genes1 = chromosome1.genes.copy()
    genes2 = chromosome2.genes.copy()
    crossover_point = 3
    child1 = Chromosome.Chromosome(genes1[:crossover_point] + genes2[:crossover_point])
    child2 = Chromosome.Chromosome(genes2[:crossover_point] + genes1[:crossover_point])

    return child1, child2

def mutation(chromosomes):
    """
    Don't forget to use Gaussian Noise here !
    :param chromosome:
    :return: mutated chromosome
    """
    for chromosome in chromosomes:
        r_val = numpy.random.normal(size=chromosome.chromosome_length)
        for idx in range(chromosome.chromosome_length):
            chromosome.genes[idx] = int(chromosome.genes[idx] + r_val[idx])
            if chromosome.genes[idx] < 0:
                chromosome.genes[idx] = 0
            if chromosome.genes[idx] > 9:
                chromosome.genes[idx] = 9
        
    return chromosomes

def evaluate_new_generation(population):  # fitness function
    """
    Call evaluate method for each new chromosome
    :return: list of chromosomes with evaluated scores
    """
    for chor in population:
        chor.evaluate()

    return population

def choose_new_generation(population):
    #Todo
    """
    Use one of the discussed methods in class.
    Q-tournament is suggested !
    :return: Mu selected chromosomes for next cycle
    """
    chosen = []
    q = int(Mu/4)
    for n in range(Mu):
        chosen_round = random.choices(population, k=q)
        winner = max(chosen_round, key=lambda item: item.score)
        chosen.append(winner)

    return chosen

def probable_crossover(parents):
    no_parents = len(parents)
    offspring = []
    p1_idx = -1
    generated_offsprings = 0
    while generated_offsprings < Lambda:
        p1_idx = (p1_idx + 1)%no_parents
        p2_idx = (p1_idx + 1)%no_parents
        if random.random() < crossover_probability:
            ch1, ch2 = crossover(parents[p1_idx], parents[p2_idx])
            offspring.append(ch1)
            offspring.append(ch2)
            generated_offsprings += 2
    if len(offspring) > Lambda:
        offspring.pop()
    
    return offspring

def calc_stat(stat_container, population):
    new_stat = {}
    new_stat['caption'] = 'generation ' + str(len(stat_container))
    new_stat['max'] = max(population, key=lambda item: item.score)
    new_stat['min'] = min(population, key=lambda item: item.score)
    new_stat['average'] = sum(chor.score for chor in population)/len(population)
    stat_container.append(new_stat)

def print_stat(stat_container):
    for population in stat_container:
        print(population['caption'])
        print('max= ' + str(population['max'].score))
        print('min= ' + str(population['min'].score))
        print('average= ' + str(population['average']))
        print('---------------------------------------')

if __name__ == '__main__':
    iterations = 15
    population = generate_initial_population()
    evaluate_new_generation(population)
    population_stat = []
    for i in range(iterations):
        calc_stat(population_stat, population)

        parents = generate_new_seed(population)
        offspring = probable_crossover(parents)
        mutation(offspring)
        population = parents + offspring
        evaluate_new_generation(population)
    
    print_stat(population_stat)
    max_of_generations = max(population_stat, key=lambda item: item['max'].score)['max']
    pca = max_of_generations.x, max_of_generations.y
    print('best solution (pca) is:')
    print(pca)
    plot.plot(pca[0], pca[1])
