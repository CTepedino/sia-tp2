import random
from typing import Callable
from PIL import Image, ImageDraw
from dataclasses import dataclass

@dataclass(frozen=True)
class Triangle:
    a: tuple[int, int]
    b: tuple[int, int]
    c: tuple[int, int]
    color: tuple[int, int, int, int]

    def points(self):
        return [self.a, self.b, self.c]

def random_triangle(width, height) -> Triangle:
    a = (random.randint(0, width - 1), random.randint(0, height - 1))
    b = (random.randint(0, width - 1), random.randint(0, height - 1))
    c = (random.randint(0, width - 1), random.randint(0, height - 1))
    rgba = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    return Triangle(a, b, c, rgba)

class Individual:
    def __init__(self, width, height, triangle_count, fitness, triangles: [Triangle]):
        self.width = width
        self.height = height
        self.triangle_count = triangle_count
        self.triangles = triangles
        self.fitness = fitness
        self.fitness_value = None
        self.cached_img = None

    def __str__(self):
        ind_string = ""
        for triangle in self.triangles:
            ind_string += f"{triangle}\n"
        return ind_string

    def __eq__(self, other):
        return self.triangles == other.triangles

    def __hash__(self):
        return hash(tuple(self.triangles))

    def copy(self):
        clone = Individual(self.width, self.height, self.triangle_count, self.fitness, self.triangles.copy())
        clone.fitness_value = self.fitness_value
        clone.cached_img = self.cached_img
        return clone

    def draw(self):
        if self.cached_img is not None:
            return self.cached_img
        base = Image.new('RGBA', (self.width, self.height), (255, 255, 255, 255))
        batch_overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(batch_overlay, 'RGBA')

        for i, triangle in enumerate(self.triangles):
            draw.polygon(triangle.points(), fill=tuple(triangle.color))
            if (i + 1) % 20 == 0 or i == len(self.triangles) - 1:
                base = Image.alpha_composite(base, batch_overlay)
                batch_overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(batch_overlay, 'RGBA')

        self.cached_img = base
        return base

    def get_fitness(self):
        if self.fitness_value is None:
            self.fitness_value = self.fitness(self)
        return self.fitness_value


class IndividualFactory:
    def __init__(self, width: int, height: int, triangle_count: int, fitness: Callable[[Individual], float]):
        self.width = width
        self.height = height
        self.triangle_count = triangle_count
        self.fitness = fitness

    def create_individual(self, triangles: [Triangle]):
        return Individual(self.width, self.height, self.triangle_count, self.fitness, triangles)

    def generation_0(self, generation_size: int):
        generation = []
        for _ in range(generation_size):
            triangles = [random_triangle(self.width, self.height) for _ in range(self.triangle_count)]
            generation.append(self.create_individual(triangles))
        return generation