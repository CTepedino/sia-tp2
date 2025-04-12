import json
import sys
import os
from datetime import datetime
import time
from PIL import Image
import mutations
import matplotlib.pyplot as plt
import numpy as np
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

    def fitness_fn(individual):
        target_image = image
        # Aseguramos que ambas imágenes estén en el mismo modo y tamaño
        generated_img = individual.draw().convert("RGB")
        target_img = target_image.convert("RGB").resize((individual.width, individual.height))

        # Convertimos a numpy arrays para cálculos rápidos
        generated_np = np.array(generated_img).astype(np.float32)
        target_np = np.array(target_img).astype(np.float32)

        # Calculamos el MSE (Error cuadrático medio)
        mse = np.mean((generated_np - target_np) ** 2)

        # El máximo MSE posible es cuando cada canal tiene el valor máximo de 255, 
        # por lo tanto (255^2) por 4 canales.
        max_mse = (255 ** 2) * 4  # 4 canales (RGBA)

        # Calculamos fitness: entre 0 (muy malo) y 1 (perfecto)
        fitness_value = 1.0 - (mse / max_mse)

        # Lo limitamos entre 0 y 1
        return max(0.0, min(fitness_value, 1.0))

    factory = IndividualFactory(width, height, triangle_count, fitness_fn)
    gen = factory.generation_0(iterations)

    mutation_name = config.get("mutation", "gen") + "_mutation"
    mutation_func = getattr(mutations, mutation_name)
    mutation_prob = config.get("mutation_prob", 0.01)

    # Crear carpeta de resultados
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_dir = os.path.join("results", f"result_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    if os.path.exists(output_dir):
        print(f"Carpeta creada correctamente: {output_dir}")
    else:
        print(f"Error: no se pudo crear la carpeta {output_dir}")

    history = []

    # Evolución de generaciones
    for gen_index in range(iterations):
        # Evaluar fitness y ordenar
        gen.sort(key=lambda ind: ind.get_fitness())
        best = gen[0]
        history.append(best.get_fitness())
        print(f"Generación {gen_index:03d} | Fitness: {best.get_fitness():.6f}")

        # Guardar imagen del mejor cada cierto intervalo
        if gen_index % image_save_interval == 0:
            output_path = os.path.join(output_dir, f"gen_{gen_index:03d}.png")
            best.draw().save(output_path)

        # Mutar la siguiente generación
        if mutation_name == "multigen_mutation":
            genes_to_mutate = config.get("genes_to_mutate", 3)
            gen = [mutation_func(ind, mutation_prob=mutation_prob, genes_to_mutate=genes_to_mutate) for ind in gen]
        else:
            gen = [mutation_func(ind, mutation_prob=mutation_prob) for ind in gen]

    # Guardar mejor imagen final
    best_final = min(gen, key=lambda ind: ind.get_fitness())
    best_final.draw().save(os.path.join(output_dir, "output_final.png"))
    print("Mejor individuo guardado como output_final.png")

    # Guardar gráfico de evolución
    plt.plot(history)
    plt.xlabel("Generación")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness")
    plt.grid()
    plt.savefig(os.path.join(output_dir, "evolucion_fitness.png"))
    print("Guardado gráfico como evolucion_fitness.png")
