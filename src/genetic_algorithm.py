import random
from typing import Callable

from src.individual import IndividualFactory


def genetic_algorithm(
    factory: IndividualFactory,
    selection_method: Callable,
    crossover_method: Callable,
    mutation_method: Callable,
    generation_method: Callable,
    cut_condition: Callable,
    generation_size: int,
    selected_parents_size: int,
    crossover_probability: float,
    mutation_probability: float
):
    generation = factory.generation_0(generation_size)

    while not cut_condition():
        selected_parents = selection_method(selected_parents_size, generation)

        children = []
        for i in range(selected_parents_size):
            if random.random() < crossover_probability:
                children.append(factory.create_individual(
                    crossover_method(
                        selected_parents[i],
                        selected_parents[(i+1)%selected_parents_size]
                    )
                ))
            else:
                children.append(selected_parents[i].copy())

        for i in range(selected_parents_size):
            children[i] = mutation_method(children[i], mutation_probability)

        generation = generation_method(selected_parents, children, selection_method)









