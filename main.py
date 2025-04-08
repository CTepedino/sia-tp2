import numpy as np
from PIL import Image, ImageDraw
import random
import os
from dataclasses import dataclass
from copy import deepcopy
import argparse

# === CONFIG POR DEFAULT ===
NUM_TRIANGLES = 200
POP_SIZE = 30
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1
ELITE_COUNT = 1

# === TRIANGLE CLASS ===
@dataclass
class Triangle:
    vertices: list
    color: list

    @staticmethod
    def random(width, height):
        vertices = [(random.randint(0, width), random.randint(0, height)) for _ in range(3)]
        color = [random.randint(0, 255) for _ in range(3)] + [random.randint(0, 128)]
        return Triangle(vertices, color)

    def mutate(self, width, height):
        if random.random() < 0.5:
            i = random.randint(0, 2)
            self.vertices[i] = (random.randint(0, width), random.randint(0, height))
        else:
            j = random.randint(0, 3)
            self.color[j] = random.randint(0, 255) if j < 3 else random.randint(0, 128)

# === INDIVIDUAL CLASS ===
class Individual:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.triangles = [Triangle.random(width, height) for _ in range(NUM_TRIANGLES)]
        self.fitness = None

    def draw(self):
        img = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img, 'RGBA')
        for triangle in self.triangles:
            draw.polygon(triangle.vertices, fill=tuple(triangle.color))
        return img.convert('RGB')

    def evaluate(self, target_img):
        generated = self.draw()
        a = np.array(generated).astype(np.float32)
        b = np.array(target_img).astype(np.float32)
        mse = np.mean((a - b) ** 2)
        self.fitness = -mse
        return self.fitness

    def crossover(self, other):
        child = Individual(self.width, self.height)
        split = random.randint(0, NUM_TRIANGLES)
        child.triangles = deepcopy(self.triangles[:split] + other.triangles[split:])
        return child

    def mutate(self):
        for triangle in self.triangles:
            if random.random() < MUTATION_RATE:
                triangle.mutate(self.width, self.height)

# === FUNCIONES GENÉTICAS ===
def generate_population(width, height):
    return [Individual(width, height) for _ in range(POP_SIZE)]

def evolve_population(pop, target_img):
    for ind in pop:
        ind.evaluate(target_img)

    pop.sort(key=lambda x: x.fitness, reverse=True)
    new_pop = pop[:ELITE_COUNT]

    while len(new_pop) < POP_SIZE:
        parent1, parent2 = random.choices(pop[:10], k=2)
        child = parent1.crossover(parent2)
        child.mutate()
        new_pop.append(child)

    return new_pop

# === CONFIG DESDE ARGPARSE ===
def parse_args():
    parser = argparse.ArgumentParser(description="Algoritmo genético para recrear una imagen con triángulos")
    parser.add_argument("--num_triangles", type=int, default=2000, help="Cantidad de triángulos por individuo")
    parser.add_argument("--pop_size", type=int, default=30, help="Tamaño de la población")
    parser.add_argument("--num_generations", type=int, default=100, help="Cantidad de generaciones")
    parser.add_argument("--mutation_rate", type=float, default=0.1, help="Tasa de mutación")
    parser.add_argument("--elite_count", type=int, default=1, help="Cantidad de individuos elite que se conservan")
    return parser.parse_args()

# === MAIN ===
def main():
    args = parse_args()

    global NUM_TRIANGLES, POP_SIZE, NUM_GENERATIONS, MUTATION_RATE, ELITE_COUNT
    NUM_TRIANGLES = args.num_triangles
    POP_SIZE = args.pop_size
    NUM_GENERATIONS = args.num_generations
    MUTATION_RATE = args.mutation_rate
    ELITE_COUNT = args.elite_count

    target = Image.open("wancho.jpeg").convert("RGB")
    width, height = target.size

    population = generate_population(width, height)

    for generation in range(NUM_GENERATIONS):
        population = evolve_population(population, target)
        best = population[0]
        print(f"Gen {generation:03d} | Fitness: {best.fitness:.2f}")

    best_img = population[0].draw()
    best_img.save("output_final.png")
    print("Mejor individuo guardado como output_final.png")

if __name__ == "__main__":
    main()
