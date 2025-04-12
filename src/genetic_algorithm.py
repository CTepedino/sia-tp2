import random
from typing import Callable

from src.individual import IndividualFactory

cut_conditions = {}

def set_time_cut_condition(max_time):
    cut_conditions["time"] = max_time

def set_generations_cut_condition(max_generations):
    cut_conditions["generations"] = max_generations

def set_acceptable_solution_cut_condition(threshold):
    cut_conditions["acceptable_solution"] = threshold

def set_unchanging_individuals_cut_condition(threshold, generations):
    cut_conditions["unchanging_individuals"] = (threshold, generations)

def set_unchanging_max_fitness_cut_condition(generations):
    cut_conditions["unchanging_max_fitness"] = generations

max_fitness = None
repeated_max_fitness = 1

similar_generations = 1

def cut_condition(run_time, generation_number, old_generation, new_generation):
    global max_fitness
    global repeated_max_fitness
    global similar_generations

    if "time" in cut_conditions:
        if run_time >= cut_conditions["time"]:
            return True
    if "generations" in cut_conditions:
        if generation_number >= cut_conditions["generations"]:
            return True

    gen_max_fitness = max(new_generation, key=lambda ind: ind.get_fitness)

    if "acceptable_solution" in cut_conditions:
        if gen_max_fitness >= "acceptable_solution":
            return True

    if "unchanging_max_fitness" in cut_conditions:
        if max_fitness is not None:
            if gen_max_fitness > max_fitness:
                repeated_max_fitness = 1
                max_fitness = gen_max_fitness
            else:
                repeated_max_fitness += 1
        else:
            max_fitness = gen_max_fitness

        if repeated_max_fitness >= cut_conditions["unchanging_max_fitness"]:
            return True

    if "unchanging_individuals" in cut_conditions:
        if old_generation is not None:
            similarity = len(set(old_generation) & set(new_generation))/len(old_generation)
            if similarity >= cut_conditions["unchanging_individuals"][0]:
                similar_generations += 1
            else:
                similar_generations = 1
            if similar_generations >= cut_conditions["unchanging_individuals"][1]:
                return True

    return False


def genetic_algorithm(
        factory: IndividualFactory,
    selection_method: Callable,
    crossover_method: Callable,
    mutation_method: Callable,
    generation_method: Callable,
    generation_size: int,
    selected_parents_size: int,
    crossover_probability: float,
    mutation_probability: float
):
    generation = factory.generation_0(generation_size)
    old_generation = None

    while not cut_condition(run_time, generation_number, old_generation, generation):
        selected_parents = selection_method(selected_parents_size, generation)
        random.shuffle(selected_parents)

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

        old_generation = generation
        generation = generation_method(generation, children, selection_method)

    return max(generation, key=lambda ind: ind.get_fitness())







