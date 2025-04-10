import random
from typing import Callable

from PIL import Image, ImageDraw

class Triangle:
    def __init__(self, a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], color: tuple[int, int, int, int]):
        self.a = a
        self.b = b
        self.c = c
        self.color = color

    def points(self):
        return [self.a,self.b,self.c]

    def __str__(self):
        return f"triangle: {self.a}, {self.b}, {self.c} - rgba: {self.color}"

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

    def __str__(self):
        ind_string = ""
        for triangle in self.triangles:
            ind_string += f"{triangle}\n"
        return ind_string

    def copy(self):
        return Individual(self.width, self.height, self.triangle_count, self.fitness, self.triangles.copy())

    def draw(self):
        canvas = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))
        overlay = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay, "RGBA")

        for triangle in self.triangles:
            draw_overlay.polygon(triangle.points(), fill=triangle.color)

        canvas = Image.alpha_composite(canvas, overlay)
        return canvas

    def get_fitness(self):
        if self.fitness_value is None:
            self.fitness_value = fitness(self)
        return self.fitness_value

def fitness(i: Individual):
    return 0 #TODO

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
        for i in range(generation_size):
            triangles = []
            for i in range(self.triangle_count):
                triangles.append(random_triangle(self.width, self.height))
            generation.append(self.create_individual(triangles))
        return generation


