import math
import random

from individual import Individual, Triangle


def single_point(i1: Individual, i2: Individual) -> [Triangle]:
    s = i1.triangle_count
    p = random.randint(0, s-1)

    return i1.triangles[:p] + i2.triangles[p:]

def double_point(i1: Individual, i2: Individual) -> [Triangle]:
    s = i1.triangle_count
    p1 = random.randint(0, s-1)
    p2 = random.randint(p1, s-1)

    return i1.triangles[:p1] + i2.triangles[p1:p2] + i1.triangles[p2:]

def ring(i1: Individual, i2: Individual) -> [Triangle]:
    s = i1.triangle_count
    p = random.randint(0, s-1)
    l = random.randint(0, math.ceil(s/2))

    triangles = i1.triangles.copy()

    for i in range(l):
        idx = (i+p)%s
        triangles[idx] = i2.triangles[idx]

    return triangles

def uniform(i1: Individual, i2: Individual) -> [Triangle]:
    triangles = []
    for i in range(i1.triangle_count):
        if random.random() < 0.5:
            triangles.append(i1.triangles[i])
        else:
            triangles.append(i2.triangles[i])

    return triangles

crossover_methods = {
    "single_point": single_point,
    "double_point": double_point,
    "ring": ring,
    "uniform": uniform,
}