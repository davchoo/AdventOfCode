from math import atan2, pi
from itertools import groupby
from more_itertools import roundrobin, nth
from operator import itemgetter


def process_data(data):
    asteroids = []
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                asteroids.append((x, y))
    return asteroids


def distance(offset):
    return pow(pow(offset[0], 2) + pow(offset[1], 2), 0.5)


# Calculate angle with
# 0 being (-1, 0) and going clockwise
def calc_angle(x, y):
    angle = -(atan2(-y, x) - pi / 2.0)
    if angle < 0:
        angle = 2 * pi + angle
    return angle


def in_line_of_sight(pos, asteroids):
    asteroids = list(filter(lambda x: x != pos, asteroids))  # Remove current asteroid
    current_x, current_y = pos
    offsets = [(x - current_x, y - current_y) for x, y in asteroids]
    polar_coords = []
    for (off_x, off_y), asteroid_pos in zip(offsets, asteroids):
        angle = calc_angle(off_x, off_y)
        radius = distance((off_x, off_y))
        polar_coords.append((angle, radius, asteroid_pos))
    polar_coords.sort(key=lambda coord: coord[0])  # Sort by angle

    visible = []
    grouped_angles = []
    for angle, coords in groupby(polar_coords, key=lambda coord: coord[0]):
        coords = list(coords)
        coords.sort(key=lambda coord: coord[1])  # Sort by distance
        grouped_angles.append(coords)

        closest = coords[0]
        visible.append(closest)

    return len(visible), grouped_angles


def locate_best_location(asteroids):
    visibility_map = {}
    for coord in asteroids:
        visibility_map[coord] = in_line_of_sight(coord, asteroids)[0]

    best_location = max(visibility_map.items(), key=itemgetter(1))
    return best_location


def solve_a(data):
    asteroids = process_data(data)
    coords, num_visible = locate_best_location(asteroids)
    return num_visible


def solve_b(data):
    asteroids = process_data(data)
    coords, num_visible = locate_best_location(asteroids)
    num_visible, grouped_angles = in_line_of_sight(coords, asteroids)
    vaporization_order = roundrobin(*grouped_angles)
    two_hundredth = nth(vaporization_order, 199)
    x, y = two_hundredth[2]
    return x * 100 + y
