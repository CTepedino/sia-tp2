import json
import os
import sys

from PIL import Image

from crossover import crossover_methods
from generation import generation_methods
from genetic_algorithm import set_time_cut_condition, set_generations_cut_condition, \
    set_acceptable_solution_cut_condition, set_unchanging_individuals_cut_condition, \
    set_unchanging_max_fitness_cut_condition, genetic_algorithm
from individual import IndividualFactory
from fitness import get_fitness_fn
from mutation import mutation_methods, set_positional_mutation_range, set_color_mutation_range
from selection import selection_methods, set_initial_temperature, set_min_temperature, \
    set_deterministic_tournament_participants, set_probabilistic_tournament_threshold

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

    print("Welcome!")
    image_file_name = config["image"]
    image = Image.open(image_file_name).convert("RGB")
    width, height = image.size

    cut_conditions = config["cut_conditions"]
    if "time" in cut_conditions:
        set_time_cut_condition(int(cut_conditions["time"]))
    if "generations" in cut_conditions:
        set_generations_cut_condition(int(cut_conditions["generations"]))
    if "acceptable_solution" in cut_conditions:
        set_acceptable_solution_cut_condition(float(config["acceptable_solution"]))
    if "unchanging_individuals" in cut_conditions:
        set_unchanging_individuals_cut_condition(float(config["unchanging_individuals"]["threshold"]),
                                                 int(config["unchanging_individuals"]["generations"]))
    if "unchanging_max_fitness" in cut_conditions:
        set_unchanging_max_fitness_cut_condition(int(config["unchanging_max_fitness"]))

    if "boltzmann_initial_temperature" in config:
        set_initial_temperature(float(config["boltzmann_initial_temperature"]))
    if "boltzmann_minimum_temperature" in config:
        set_min_temperature(float(config["boltzmann_minimum_temperature"]))

    if "deterministic_tournament_participants" in config:
        set_deterministic_tournament_participants(config["deterministic_tournament_participants"])

    if "probabilistic_tournament_threshold" in config:
        set_probabilistic_tournament_threshold(config["probabilistic_tournament_threshold"])

    factory = IndividualFactory(
        width=width,
        height=height,
        triangle_count=int(config["triangle_count"]),
        fitness=get_fitness_fn(image)
    )

    best_individual = genetic_algorithm(
        factory=factory,
        selection_method=selection_methods[config["selection_method"]],
        crossover_method=crossover_methods[config["crossover_method"]],
        mutation_method=mutation_methods[config["mutation_method"]],
        generation_method=generation_methods[config["generation_method"]],
        generation_size=config["generation_size"],
        selected_parents_size=config["selected_parents_size"],
        crossover_probability=config["crossover_probability"],
        mutation_probability=config["mutation_probability"]
    )


    output_image = best_individual.draw()
    output_path = os.path.join(os.path.dirname(image_file_name), "output.png")
    output_image.save(output_path)
    print(f"Fitness = {best_individual.get_fitness()}")




