import json
import sys

from PIL import Image

from individual import IndividualFactory

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        config = json.load(f)

    image_file_name = config["image"]
    triangle_count = int(config["triangle_count"])

    compressed_name = f"{triangle_count}_triangles_{image_file_name}"

    image = Image.open(image_file_name).convert("RGBA")
    width, height = image.size

    factory = IndividualFactory(width, height, triangle_count, lambda x: 0)

    gen = factory.generation_0(10)

    for i, individual in enumerate(gen):
        individual.draw().save(f"canvas_{i}.png")






