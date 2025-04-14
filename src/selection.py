import math
import random

from individual import Individual

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

    pseudo_fitness_sum = 0
    for i in range(n):
        pseudo_fitness_sum += pseudo_fitness(i)

    def relative_pseudo_fitness(index):
        return pseudo_fitness(index)/pseudo_fitness_sum

    accumulated_fitness = []
    accum = 0
    for i in range(n):
        accum += relative_pseudo_fitness(i)
        accumulated_fitness.append(accum)

    selected = []
    for _ in range(k):
        r = random.random()
        for i, accum in enumerate(accumulated_fitness):
            if r <= accum:
                selected.append(individuals[i].copy())
                break
    return selected

_temperature = 1
_initial_temperature = _temperature
_min_temperature = 0.5
_generation = 0

def set_initial_temperature(value):
    global _temperature
    global _initial_temperature
    _temperature = value
    _initial_temperature = value

def set_min_temperature(value):
    global _min_temperature
    _min_temperature = value

def evolve_temperature():
    global _temperature
    global _generation

    _generation += 1
    _temperature = _min_temperature + (_initial_temperature - _min_temperature)*math.exp(-_temperature)



def boltzmann(k: int, individuals: [Individual]) -> [Individual]:
    temperature = _temperature

    n = len(individuals)

    population_averages = sum(map(lambda i: math.exp(i.get_fitness()/temperature), individuals))/n
    def pseudo_fitness(individual):
        return math.exp(individual.get_fitness()/temperature)/population_averages

    pseudo_fitness_sum = 0
    for individual in individuals:
        pseudo_fitness_sum += pseudo_fitness(individual)

    def relative_pseudo_fitness(individual):
        return pseudo_fitness(individual)/pseudo_fitness_sum

    accumulated_fitness = []
    accum = 0
    for individual in individuals:
        accum += relative_pseudo_fitness(individual)
        accumulated_fitness.append(accum)


    evolve_temperature()

    selected = []
    for _ in range(k):
        r = random.random()
        for i, accum in enumerate(accumulated_fitness):
            if r <= accum:
                selected.append(individuals[i].copy())
                break
    return selected

_deterministic_tournament_participants = 10
def set_deterministic_tournament_participants(value):
    global _deterministic_tournament_participants
    _deterministic_tournament_participants = value

def deterministic_tournament(k: int, individuals: [Individual]):
    selected = []
    for _ in range(k):
        participants = random.choices(individuals, k=_deterministic_tournament_participants)
        selected.append(max(participants, key=lambda i: i.get_fitness()).copy())

    return selected


_threshold = 0.75
def set_probabilistic_tournament_threshold(value):
    global _threshold
    _threshold = value

def probabilistic_tournament(k: int, individuals: [Individual]):
    selected = []
    for _ in range(k):
        participants = random.choices(individuals, k=2)
        r = random.random()
        if r < _threshold:
            selected.append(max(participants, key=lambda i: i.get_fitness()).copy())
        else:
            selected.append(min(participants, key=lambda i: i.get_fitness()).copy())
    return selected

selection_methods = {
    "elite": elite,
    "roulette": roulette,
    "universal": universal,
    "ranking": ranking,
    "boltzmann": boltzmann,
    "deterministic_tournament": deterministic_tournament,
    "probabilistic_tournament": probabilistic_tournament
}