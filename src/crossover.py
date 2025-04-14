import math
import random

from individual import Individual, Triangle


def single_point(i1: Individual, i2: Individual):
    s = i1.triangle_count
    p = random.randint(0, s-1)

    return i1.triangles[:p] + i2.triangles[p:], i2.triangles[:p] + i1.triangles[p:]

def double_point(i1: Individual, i2: Individual):
    s = i1.triangle_count
    p1 = random.randint(0, s-1)
    p2 = random.randint(p1, s-1)

    return i1.triangles[:p1] + i2.triangles[p1:p2] + i1.triangles[p2:], i2.triangles[:p1] + i1.triangles[p1:p2] + i2.triangles[p2:]

def ring(i1: Individual, i2: Individual):
    s = i1.triangle_count
    p = random.randint(0, s-1)
    l = random.randint(0, math.ceil(s/2))

    trianglesA = i1.triangles.copy()
    trianglesB = i2.triangles.copy()

    for i in range(l):
        idx = (i+p)%s
        trianglesA[idx] = i2.triangles[idx]
        trianglesB[idx] = i1.triangles[idx]

    return trianglesA, trianglesB

def uniform(i1: Individual, i2: Individual):
    trianglesA = []
    trianglesB = []
    for i in range(i1.triangle_count):
        if random.random() < 0.5:
            trianglesA.append(i1.triangles[i])
            trianglesB.append(i2.triangles[i])
        else:
            trianglesA.append(i2.triangles[i])
            trianglesB.append(i1.triangles[i])

    return trianglesA, trianglesB

crossover_methods = {
    "single_point": single_point,
    "double_point": double_point,
    "ring": ring,
    "uniform": uniform,
}