
from PIL import Image
from skimage.util import img_as_float
from skimage.metrics import structural_similarity as ssim
import numpy as np

def get_fitness_fn(image: Image):

    target_np = img_as_float(np.array(image))

    def fitness(individual):
        generated_image = individual.draw().convert("RGB")

        generated_np = img_as_float(np.array(generated_image))

        return ssim(generated_np, target_np, channel_axis=-1, data_range=1.0)

    return fitness
