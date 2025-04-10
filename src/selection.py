import math
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
            selected.append(individual)
            times += 1

    return selected

def relative_fitness(individual: Individual, individuals: [Individual]):
    return individual.get_fitness() / sum(map(lambda i: i.get_fitness(), individuals))

def roulette(k: int, individuals: [Individual]) -> [Individual]:
    return None


selection_methods = {
    "elite": elite,
    "roulette": roulette
}