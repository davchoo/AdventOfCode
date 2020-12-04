from itertools import count
from functools import reduce
import operator


def process_data(data):
    area = {}
    for y, line in enumerate(data.splitlines()):
        area["width"] = len(line)
        area["height"] = y + 1  # This stores the correct height when it finishes
        for x, tile in enumerate(line):
            area[(x, y)] = tile
    return area


def get_tile(tile_map: dict, x: int, y: int):
    return tile_map[(x % tile_map["width"], y)]  # The map repeats horizontally infinitely


def check_slope(tile_map: dict, x_slope: int, y_slope: int):
    num_trees = 0
    for x, y in zip(count(0, x_slope), range(0, tile_map["height"], y_slope)):
        tile = get_tile(tile_map, x, y)
        if tile == "#":
            num_trees += 1
    return num_trees


def solve_a(data):
    tile_map = process_data(data)
    return check_slope(tile_map, 3, 1)


def solve_b(data):
    tile_map = process_data(data)
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = [check_slope(tile_map, *slope) for slope in slopes]
    return reduce(operator.mul, trees)
