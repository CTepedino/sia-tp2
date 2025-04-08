import numpy as np
from PIL import Image, ImageDraw
import random
from dataclasses import dataclass
from copy import deepcopy
import argparse
import matplotlib.pyplot as plt

# === CONFIG POR DEFAULT ===
NUM_TRIANGLES = 200
POP_SIZE = 30
NUM_GENERATIONS = 500
MUTATION_RATE = 0.1
ELITE_COUNT = 1

# === TRIANGLE CLASS ===
@dataclass
class Triangle:
    vertices: list
    color: list

    @staticmethod
    def random(width, height, max_size=50):
        cx = random.randint(0, width)
        cy = random.randint(0, height)
        vertices = []
        for _ in range(3):
            dx = random.randint(-max_size, max_size)
            dy = random.randint(-max_size, max_size)
            x = min(max(cx + dx, 0), width)
            y = min(max(cy + dy, 0), height)
            vertices.append((x, y))
        color = [random.randint(0, 255) for _ in range(3)] + [random.randint(60, 120)]
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
        base = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))

        batch_overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(batch_overlay, 'RGBA')

        for i, triangle in enumerate(self.triangles):
            draw.polygon(triangle.vertices, fill=tuple(triangle.color))

            if (i + 1) % 10 == 0 or i == len(self.triangles) - 1:
                base = Image.alpha_composite(base, batch_overlay)
                batch_overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(batch_overlay, 'RGBA')

        return base

    def evaluate(self, target_img):
        generated = self.draw()
        a = np.array(generated.convert("RGB")).astype(np.float32)
        b = np.array(target_img.convert("RGB")).astype(np.float32)
        mse = np.mean((a - b) ** 2)
        self.fitness = -mse
        return self.fitness

    def crossover(self, other):
        child = Individual(self.width, self.height)
        split = random.randint(0, NUM_TRIANGLES)
        child.triangles = deepcopy(self.triangles[:split] + other.triangles[split:])
        return child

# === FUNCIONES DE MEJORA ===
def select_parents(pop, method="elite"):
    if method == "elite":
        return random.choices(pop[:10], k=2)
    elif method == "ruleta":
        min_fitness = min(ind.fitness for ind in pop)
        offset = abs(min_fitness) + 1e-6
        probs = [(ind.fitness + offset) for ind in pop]
        return random.choices(pop, weights=probs, k=2)
    elif method == "torneo":
        k = 5
        return [max(random.sample(pop, k), key=lambda x: x.fitness) for _ in range(2)]

def crossover_two_points(p1, p2):
    i, j = sorted(random.sample(range(NUM_TRIANGLES), 2))
    child = Individual(p1.width, p1.height)
    child.triangles = deepcopy(p1.triangles[:i] + p2.triangles[i:j] + p1.triangles[j:])
    return child

def crossover_uniform(p1, p2):
    child = Individual(p1.width, p1.height)
    child.triangles = [
        deepcopy(random.choice([t1, t2]))
        for t1, t2 in zip(p1.triangles, p2.triangles)
    ]
    return child

def mutate_gene(ind):
    idx = random.randint(0, NUM_TRIANGLES - 1)
    ind.triangles[idx].mutate(ind.width, ind.height)

def mutate_multigen(ind, rate=0.1):
    for tri in ind.triangles:
        if random.random() < rate:
            tri.mutate(ind.width, ind.height)

# === EVOLUCIÓN ===
def evolve_population(pop, target_img, args):
    for ind in pop:
        ind.evaluate(target_img)

    pop.sort(key=lambda x: x.fitness, reverse=True)
    new_pop = pop[:ELITE_COUNT]

    while len(new_pop) < POP_SIZE:
        parent1, parent2 = select_parents(pop, method=args.selection)

        if args.crossover == "one_point":
            child = parent1.crossover(parent2)
        elif args.crossover == "two_points":
            child = crossover_two_points(parent1, parent2)
        elif args.crossover == "uniform":
            child = crossover_uniform(parent1, parent2)

        if args.mutation == "simple":
            child.mutate()
        elif args.mutation == "gene":
            mutate_gene(child)
        elif args.mutation == "multigen":
            mutate_multigen(child, rate=args.mutation_rate)

        new_pop.append(child)

    return new_pop

def evolve_population_young_bias(pop, target_img, args):
    for ind in pop:
        ind.evaluate(target_img)
    pop.sort(key=lambda x: x.fitness, reverse=True)

    new_pop = pop[:ELITE_COUNT]

    while len(new_pop) < POP_SIZE:
        if random.random() < 0.7:
            parent1, parent2 = select_parents(pop[:10], method=args.selection)
        else:
            parent1, parent2 = select_parents(pop, method=args.selection)

        if args.crossover == "one_point":
            child = parent1.crossover(parent2)
        elif args.crossover == "two_points":
            child = crossover_two_points(parent1, parent2)
        elif args.crossover == "uniform":
            child = crossover_uniform(parent1, parent2)

        if args.mutation == "simple":
            child.mutate()
        elif args.mutation == "gene":
            mutate_gene(child)
        elif args.mutation == "multigen":
            mutate_multigen(child, rate=args.mutation_rate)

        new_pop.append(child)

    return new_pop

# === CONFIG Y MAIN ===
def generate_population(width, height):
    return [Individual(width, height) for _ in range(POP_SIZE)]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", type=str, required=True, help="Ruta a la imagen a aproximar")
    parser.add_argument("--num_triangles", type=int, default=200)
    parser.add_argument("--pop_size", type=int, default=30)
    parser.add_argument("--num_generations", type=int, default=50)
    parser.add_argument("--mutation_rate", type=float, default=0.1)
    parser.add_argument("--elite_count", type=int, default=1)
    parser.add_argument("--selection", type=str, default="elite", choices=["elite", "ruleta", "torneo"])
    parser.add_argument("--crossover", type=str, default="one_point", choices=["one_point", "two_points", "uniform"])
    parser.add_argument("--mutation", type=str, default="simple", choices=["simple", "gene", "multigen"])
    parser.add_argument("--young_bias", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    global NUM_TRIANGLES, POP_SIZE, NUM_GENERATIONS, MUTATION_RATE, ELITE_COUNT
    NUM_TRIANGLES = args.num_triangles
    POP_SIZE = args.pop_size
    NUM_GENERATIONS = args.num_generations
    MUTATION_RATE = args.mutation_rate
    ELITE_COUNT = args.elite_count

    target = Image.open(args.image_path).convert("RGB")
    width, height = target.size
    population = generate_population(width, height)

    evolve_fn = evolve_population_young_bias if args.young_bias else evolve_population
    history = []

    for generation in range(NUM_GENERATIONS):
        population = evolve_fn(population, target, args)
        best = population[0]
        history.append(-best.fitness)
        print(f"Gen {generation:03d} | Fitness: {best.fitness:.2f}")

        if generation % 5 == 0:
            img = best.draw().convert("RGB")
            img.save(f"gen_{generation:03d}.png")

    best_img = population[0].draw().convert("RGB")
    best_img.save("output_final.png")
    print("Mejor individuo guardado como output_final.png")

    plt.plot(history)
    plt.xlabel("Generación")
    plt.ylabel("Error (MSE)")
    plt.title("Evolución del Error")
    plt.grid()
    plt.savefig("evolucion_fitness.png")
    print("Guardado gráfico como evolucion_fitness.png")

if __name__ == "__main__":
    main()
