import json
import sys
import os
from datetime import datetime
import time
from PIL import Image
import mutations  # Import general para elegir la función según config
from individual import IndividualFactory

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

    image_file_name = config["image"]
    triangle_count = int(config["triangle_count"])
    iterations = int(config["iterations"])
    image_save_interval = int(config["image_save_interval"])

    compressed_name = f"{triangle_count}_triangles_{image_file_name}"

    image = Image.open(image_file_name).convert("RGBA")
    width, height = image.size

    factory = IndividualFactory(width, height, triangle_count, lambda x: 0)
    gen = factory.generation_0(iterations)

    # Obtener nombre de mutación y función correspondiente
    mutation_name = config.get("mutation", "gen") + "_mutation"
    mutation_func = getattr(mutations, mutation_name)
    mutation_prob = config.get("mutation_prob", 0.01)

    # Aplicar la mutación según el tipo
    if mutation_name == "multigen_mutation":
        genes_to_mutate = config.get("genes_to_mutate", 3)
        gen = [mutation_func(ind, mutation_prob=mutation_prob, genes_to_mutate=genes_to_mutate) for ind in gen]
    else:
        gen = [mutation_func(ind, mutation_prob=mutation_prob) for ind in gen]

    # Crear carpeta de resultados
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = os.path.join("results", f"result_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_dir):
        print(f"Carpeta creada correctamente: {output_dir}")
    else:
        print(f"Error: no se pudo crear la carpeta {output_dir}")

    # Guardar imágenes de la generación
    for i, individual in enumerate(gen):
        if i % image_save_interval == 0:
            output_path = os.path.join(output_dir, f"canvas_{i}.png")
            individual.draw().save(output_path)
