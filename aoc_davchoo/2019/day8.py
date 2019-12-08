import collections
from operator import itemgetter
from PIL import Image
import numpy as np


def process_data(data):
    image_data = list(map(int, data))
    width = 25
    height = 6
    layers = len(image_data) // width // height
    image = collections.defaultdict(dict)
    for layer in range(layers):
        for y in range(height):
            for x in range(width):
                image[layer][x, y] = image_data[x + y * width + layer * width * height]
    return image


def solve_a(data):
    image = process_data(data)
    num_digits = [collections.Counter(layer.values()) for layer in image.values()]
    num_zeros = [(i, count[0]) for i, count in enumerate(num_digits)]
    min_zeros_layer = min(num_zeros, key=itemgetter(1))[0]
    return num_digits[min_zeros_layer][1] * num_digits[min_zeros_layer][2]


def solve_b(data):
    image = process_data(data)
    width = 25
    height = 6
    layers = len(image.keys())
    final_image = np.zeros((height, width, 3), dtype=np.uint8)
    color_palette = [[0, 0, 0], [255, 255, 255]]
    for y in range(height):
        for x in range(width):
            colors = [image[layer][x, y] for layer in range(layers)]
            colors = filter(lambda color: color != 2, colors)
            final_color: int = next(colors)
            final_image[y, x] = color_palette[final_color]
    img = Image.fromarray(final_image, 'RGB')
    img.save('day8.png')
    img.show()
    return 0
