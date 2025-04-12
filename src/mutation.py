import random
from individual import Individual




def gen_mutation(individual: Individual, mutation_prob=0.01, mutation_range=30) -> Individual:
    mutated = individual.copy()
    if random.random() < mutation_prob:
        tri = random.choice(mutated.triangles)
        attr = random.randint(0, 9)
        if attr < 6:
            point_idx = attr // 2
            coord_idx = attr % 2
            point = list(tri.points()[point_idx])
            old_val = point[coord_idx]
            limit = mutated.width if coord_idx == 0 else mutated.height
            delta = random.randint(-mutation_range, mutation_range)
            new_val = min(max(0, old_val + delta), limit - 1)
            point[coord_idx] = new_val
            if point_idx == 0:
                tri.a = tuple(point)
            elif point_idx == 1:
                tri.b = tuple(point)
            else:
                tri.c = tuple(point)
        else:
            color = list(tri.color)
            idx = attr - 6
            old_val = color[idx]
            delta = random.randint(-mutation_range, mutation_range)
            color[idx] = min(max(0, old_val + delta), 255)
            tri.color = tuple(color)
    return mutated



def multigen_mutation(individual: Individual, mutation_prob=0.05, genes_to_mutate=3, mutation_range=30) -> Individual:
    mutated = individual.copy()
    for _ in range(genes_to_mutate):
        if random.random() < mutation_prob:
            tri = random.choice(mutated.triangles)
            attr = random.randint(0, 9)
            if attr < 6:
                point_idx = attr // 2
                coord_idx = attr % 2
                point = list(tri.points()[point_idx])
                old_val = point[coord_idx]
                limit = mutated.width if coord_idx == 0 else mutated.height
                delta = random.randint(-mutation_range, mutation_range)
                new_val = min(max(0, old_val + delta), limit - 1)
                point[coord_idx] = new_val
                if point_idx == 0:
                    tri.a = tuple(point)
                elif point_idx == 1:
                    tri.b = tuple(point)
                else:
                    tri.c = tuple(point)
            else:
                color = list(tri.color)
                idx = attr - 6
                old_val = color[idx]
                delta = random.randint(-mutation_range, mutation_range)
                color[idx] = min(max(0, old_val + delta), 255)
                tri.color = tuple(color)
    return mutated



def uniform_mutation(individual: Individual, mutation_prob=0.01, mutation_range=30) -> Individual:
    mutated = individual.copy()
    for tri in mutated.triangles:
        for idx, point in enumerate([tri.a, tri.b, tri.c]):
            x, y = point
            if random.random() < mutation_prob:
                delta = random.randint(-mutation_range, mutation_range)
                x = min(max(0, x + delta), mutated.width - 1)
            if random.random() < mutation_prob:
                delta = random.randint(-mutation_range, mutation_range)
                y = min(max(0, y + delta), mutated.height - 1)
            if idx == 0:
                tri.a = (x, y)
            elif idx == 1:
                tri.b = (x, y)
            else:
                tri.c = (x, y)
        color = list(tri.color)
        for i in range(4):
            if random.random() < mutation_prob:
                delta = random.randint(-mutation_range, mutation_range)
                color[i] = min(max(0, color[i] + delta), 255)
        tri.color = tuple(color)
    return mutated


mutation_methods = {
    "gen_mutation": gen_mutation,
    "multigen_mutation": multigen_mutation,
    "uniform_mutation": uniform_mutation,
    "complete_mutation": complete_mutation
}