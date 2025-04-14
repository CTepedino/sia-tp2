import random
from individual import Individual, Triangle, random_triangle

positional_mutation_range = 1000
color_mutation_range = 255

# def set_positional_mutation_range(value):
#     global positional_mutation_range
#     positional_mutation_range = value
#
# def set_color_mutation_range(value):
#     global color_mutation_range
#     color_mutation_range = value


def mutate_triangle(individual: Individual, triangle: Triangle):
    return random_triangle(individual.width, individual.height)

# def mutate_triangle(individual: Individual, triangle: Triangle):
#     a, b, c = triangle.points()
#     color = list(triangle.color)
#
#     if random.random() < 0.5:
#         attr = random.randint(0, 2)
#         point_idx = attr // 2
#         coord_idx = attr % 2
#         point = list(triangle.points()[point_idx])
#         old_val = point[coord_idx]
#         limit = individual.width if coord_idx == 0 else individual.height
#         delta = random.randint(-positional_mutation_range, positional_mutation_range)
#         new_val = min(max(0, old_val + delta), limit - 1)
#         point[coord_idx] = new_val
#         if point_idx == 0:
#             a = tuple(point)
#         elif point_idx == 1:
#             b = tuple(point)
#         else:
#             c = tuple(point)
#     else:
#         idx = random.randint(0, 3)
#         old_val = color[idx]
#         delta = random.randint(-color_mutation_range, color_mutation_range)
#         color[idx] = min(max(0, old_val + delta), 255)
#
#
#     return Triangle(a, b, c, (color[0], color[1], color[2], color[3]))

def gen_mutation(individual: Individual, mutation_probability) -> [Triangle]:
    mutated_triangles = individual.triangles.copy()

    if random.random() < mutation_probability:
        i = random.randint(0, individual.triangle_count -1)
        mutated_triangles[i] = mutate_triangle(individual, individual.triangles[i])

    return mutated_triangles


def multigen_mutation(individual: Individual, mutation_probabilty) -> [Triangle]:
    mutated_triangles = individual.triangles.copy()

    if random.random() < mutation_probabilty:
        mutation_count = random.randint(1, individual.triangle_count)
        to_mutate = random.sample(range(individual.triangle_count), mutation_count)
        for i in to_mutate:
            mutated_triangles[i] = mutate_triangle(individual, individual.triangles[i])

    return mutated_triangles

def uniform_mutation(individual: Individual, mutation_probability) -> [Triangle]:
    mutated_triangles = individual.triangles.copy()

    for i in range(individual.triangle_count):
        if random.random() < mutation_probability:
            mutated_triangles[i] = mutate_triangle(individual, individual.triangles[i])

    return mutated_triangles

def complete_mutation(individual: Individual, mutation_probability) -> [Triangle]:
    mutated_triangles = individual.triangles.copy()

    if random.random() < mutation_probability:
        for i in range(individual.triangle_count):
            mutated_triangles[i] = mutate_triangle(individual, individual.triangles[i])

    return mutated_triangles

mutation_methods = {
    "gen_mutation": gen_mutation,
    "multigen_mutation": multigen_mutation,
    "uniform_mutation": uniform_mutation,
    "complete_mutation": complete_mutation
}