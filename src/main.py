import json
import sys
import os
from datetime import datetime
from PIL import Image
import numpy as np
from individual import IndividualFactory
from mutation import mutation_methods
from crossover import crossover_methods
from selection import selection_methods
from generation import generation_methods
from genetic_algorithm import genetic_algorithm, set_time_cut_condition, set_generations_cut_condition, set_acceptable_solution_cut_condition, set_unchanging_individuals_cut_condition, set_unchanging_max_fitness_cut_condition
from skimage import data, img_as_float
from skimage.metrics import structural_similarity as ssim

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

    image_file_name = config["image"]
    image = Image.open(image_file_name).convert("RGBA")
    width, height = image.size

    def fitness_fn(individual):
        target_image = image
        # Aseguramos que ambas imágenes estén en el mismo modo y tamaño
        generated_img = individual.draw().convert("RGB")
        target_img = target_image.convert("RGB")


        # Convertimos a numpy arrays como float entre 0 y 1
        generated_np = img_as_float(np.array(generated_img))
        target_np = img_as_float(np.array(target_img))


        # Calculamos SSIM
        ssim_value = ssim(generated_np, target_np, channel_axis=-1, data_range=1.0)

        # Fitness entre 0 y 1 directamente
        return max(0.0, min(ssim_value, 1.0))

    factory = IndividualFactory(
        width=width,
        height=height,
        triangle_count=int(config["triangle_count"]),
        fitness=fitness_fn
    )

    cut_condition = config["cut_condition"]
    if cut_condition == "time":
        set_time_cut_condition(config["time"])
    elif cut_condition == "generations":
        set_generations_cut_condition(config["generations"])
    elif cut_condition == "acceptable_solution":
        set_acceptable_solution_cut_condition(config["acceptable_solution"])
    elif cut_condition == "unchanging_individuals":
        set_unchanging_individuals_cut_condition(config["unchanging_individuals_threshold"], config["unchanging_individuals_generations"])
    elif cut_condition == "unchanging_max_fitness":
        set_unchanging_max_fitness_cut_condition(config["unchanging_max_fitness_generations"])

    best_individual = genetic_algorithm(
        factory=factory,
        selection_method=selection_methods[config["selection_method"]],
        crossover_method=crossover_methods[config["crossover_method"]],
        mutation_method=mutation_methods[config["mutation"]],
        generation_method=generation_methods[config["generation_method"]],
        generation_size=config["generation_size"],
        selected_parents_size=config["selected_parents_size"],
        crossover_probability=config["crossover_probability"],
        mutation_probability=config["mutation_prob"]
    )

    output_image = best_individual.draw()
    output_path = os.path.join(os.path.dirname(image_file_name), "output.png")
    output_image.save(output_path)
    print(f"Best individual saved to {output_path}")
    print(f"Fitness = {best_individual.get_fitness()}")


