import random
import time
import json
import os
import matplotlib.pyplot as plt
from typing import Callable

from individual import IndividualFactory
from concurrent.futures import ThreadPoolExecutor

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

    if "time" in cut_conditions and run_time >= cut_conditions["time"]:
        return True

    if "generations" in cut_conditions and generation_number >= cut_conditions["generations"]:
        return True

    gen_max_fitness = max(new_generation, key=lambda ind: ind.get_fitness())

    if "acceptable_solution" in cut_conditions and gen_max_fitness.get_fitness() >= cut_conditions["acceptable_solution"]:
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

    if "unchanging_individuals" in cut_conditions and old_generation is not None:
        similarity = len(set(old_generation) & set(new_generation)) / len(old_generation)
        if similarity >= cut_conditions["unchanging_individuals"][0]:
            similar_generations += 1
        else:
            similar_generations = 1
        if similar_generations >= cut_conditions["unchanging_individuals"][1]:
            return True

    return False

def parallel_fitness_evaluation(generation):
    with ThreadPoolExecutor() as executor:
        list(executor.map(lambda ind: ind.get_fitness(), generation))


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
    generation_number = 0

    start_time = time.time()
    run_time = 0

    fitness_history = []

    while not cut_condition(run_time, generation_number, old_generation, generation):

        parallel_fitness_evaluation(generation)

        selected_parents = selection_method(selected_parents_size, generation)
        random.shuffle(selected_parents)

        children = []
        i = 0
        while len(children) < selected_parents_size:
            i = (i+2) % selected_parents_size
            if random.random() < crossover_probability:
                cross1, cross2 = crossover_method(
                    selected_parents[i],
                    selected_parents[(i + 1) % selected_parents_size]
                )
                children.append(factory.create_individual(cross1))
                children.append(factory.create_individual(cross2))
            else:
                children.append(selected_parents[i].copy())
                children.append(selected_parents[(i + 1) % selected_parents_size].copy())

        for i in range(selected_parents_size):
            children[i] = factory.create_individual(mutation_method(children[i], mutation_probability))

        old_generation = generation
        generation = generation_method(generation, children, selection_method)
        generation_number += 1

        print(f"generation {generation_number}")

        best_individual = max(generation, key=lambda ind: ind.get_fitness())
        fitness_history.append(best_individual.get_fitness())
        run_time = time.time() - start_time

    # Crear carpeta results si no existe
    os.makedirs("results", exist_ok=True)

    # Nombres de archivos
    base_filename = f"fitness_S{selection_method.__name__}_C{crossover_method.__name__}_M{mutation_method.__name__}_G{generation_method.__name__}"
    json_filename = os.path.join("results", base_filename + ".json")
    image_filename = os.path.join("results", base_filename + "_evolucion_fitness.png")

    # Guardar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, label="Mejor Fitness")
    plt.xlabel("Generación")
    plt.ylabel("Mejor Fitness")
    plt.title("Evolución del Fitness")
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 1)
    plt.savefig(image_filename)

    # Guardar historial en JSON
    with open(json_filename, 'w') as f:
        json.dump(fitness_history, f, indent=2)

    return max(generation, key=lambda ind: ind.get_fitness())






