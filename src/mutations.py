import random
from typing import Callable
from individual import Individual, Triangle

def gen_mutation(individual: Individual, mutation_prob=0.01) -> Individual:
    mutated = individual.copy()
    if random.random() < mutation_prob:
        tri = random.choice(mutated.triangles)
        attr = random.randint(0, 9)
        if attr < 6:
            point_idx = attr // 2
            coord_idx = attr % 2
            new_val = random.randint(0, mutated.width - 1 if coord_idx == 0 else mutated.height - 1)
            point = list(tri.points()[point_idx])
            point[coord_idx] = new_val
            if point_idx == 0:
                tri.a = tuple(point)
            elif point_idx == 1:
                tri.b = tuple(point)
            else:
                tri.c = tuple(point)
        else:
            color = list(tri.color)
            color[attr - 6] = random.randint(0, 255)
            tri.color = tuple(color)
    return mutated


def multigen_mutation(individual: Individual, mutation_prob=0.05, genes_to_mutate=3) -> Individual:
    mutated = individual.copy()
    for _ in range(genes_to_mutate):
        if random.random() < mutation_prob:
            tri = random.choice(mutated.triangles)
            attr = random.randint(0, 9)
            if attr < 6:
                point_idx = attr // 2
                coord_idx = attr % 2
                new_val = random.randint(0, mutated.width - 1 if coord_idx == 0 else mutated.height - 1)
                point = list(tri.points()[point_idx])
                point[coord_idx] = new_val
                if point_idx == 0:
                    tri.a = tuple(point)
                elif point_idx == 1:
                    tri.b = tuple(point)
                else:
                    tri.c = tuple(point)
            else:
                color = list(tri.color)
                color[attr - 6] = random.randint(0, 255)
                tri.color = tuple(color)
    return mutated


def uniform_mutation(individual: Individual, mutation_prob=0.01) -> Individual:
    mutated = individual.copy()
    for tri in mutated.triangles:
        for idx, point in enumerate([tri.a, tri.b, tri.c]):
            x, y = point
            if random.random() < mutation_prob:
                x = random.randint(0, mutated.width - 1)
            if random.random() < mutation_prob:
                y = random.randint(0, mutated.height - 1)
            if idx == 0:
                tri.a = (x, y)
            elif idx == 1:
                tri.b = (x, y)
            else:
                tri.c = (x, y)
        color = list(tri.color)
        for i in range(4):
            if random.random() < mutation_prob:
                color[i] = random.randint(0, 255)
        tri.color = tuple(color)
    return mutated


