import math
import random

from src.individual import Individual

def elite(k: int, individuals: [Individual]) -> [Individual]:
    individuals.sort(key=lambda i: i.get_fitness(), reverse=True)

    def n(index):
        return math.ceil((k - index)/len(individuals))

    selected = []
    for i, individual in enumerate(individuals):
        if len(selected) == k:
            break
        max_times = n(i)
        times = 0
        while times < max_times and len(selected) < k:
            selected.append(individual.copy())
            times += 1

    return selected

def relative_fitness(individual: Individual, individuals: [Individual]):
    return individual.get_fitness() / sum(map(lambda i: i.get_fitness(), individuals))

def accumulated_relative_fit(individuals: [Individual]):
    accum = 0
    accumulated_fitness = []
    for individual in individuals:
        accum += relative_fitness(individual, individuals)
        accumulated_fitness.append(accum)
    return accumulated_fitness

def roulette(k: int, individuals: [Individual]) -> [Individual]:
    accumulated_fitness = accumulated_relative_fit(individuals)

    selected = []
    for _ in range(k):
        r = random.random()
        for i, accum in enumerate(accumulated_fitness):
            if r <= accum:
                selected.append(individuals[i].copy())
                break
    return selected

def universal(k: int, individuals: [Individual]) -> [Individual]:
    accumulated_fitness = accumulated_relative_fit(individuals)

    r = random.random()
    r_j = r/k

    selected = []
    start = 0
    for _ in range(k):
        for i, accum in enumerate(accumulated_fitness, start):
            if r <= accum:
                selected.append(individuals[i].copy())
                start = i
                break
        r_j += 1/k

    return selected

def ranking(k: int, individuals: [Individual]) -> [Individual]:
    individuals.sort(key=lambda i: i.get_fitness(), reverse=True)
    n = len(individuals)
    def pseudo_fitness(index):
        return (n-index-1)/n
    


def boltzmann():
    return 0 #TODO

def deterministic_tournament():
    return 0 #TODO

def probabilistic_tournament():
    return 0 #TODO

selection_methods = {
    "elite": elite,
    "roulette": roulette,
    "universal": universal,
    "ranking": ranking,
    "boltzmann": boltzmann,
    "deterministic_tournament": deterministic_tournament,
    "probabilistic_tournament": probabilistic_tournament
}