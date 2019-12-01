from operator import itemgetter, sub
import collections

def process_data(data: str):
    coords = data.splitlines()
    return list(map(lambda x: tuple(map(int, x.split(","))), coords))


def manhattan_distance(coord1, coord2):
    return abs(coord2[0] - coord1[0]) + abs(coord2[1] - coord1[1])


def area_bounds(coords):
    max_x = max(coords, key=itemgetter(0))[0]
    max_y = max(coords, key=itemgetter(1))[1]
    min_x = min(coords, key=itemgetter(0))[0]
    min_y = min(coords, key=itemgetter(1))[1]
    return max_x, max_y, min_x, min_y


def solve_a(data):
    coords = process_data(data)
    # The outer coords wouldn't create closed areas
    max_x, max_y, min_x, min_y = area_bounds(coords)
    area_map = {}
    edge_coords = set()
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = {coord: manhattan_distance(coord, (x, y)) for coord in coords}
            min_coord, min_distance = min(distances.items(), key=itemgetter(1))
            if list(distances.values()).count(min_distance) == 1:
                area_map[x, y] = min_coord
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    edge_coords.add(min_coord)
            else:
                area_map[x, y] = None

    check_coords = set(coords) - edge_coords
    area = collections.Counter(area_map.values()).items()
    area = filter(lambda x: x[0] in check_coords, area)
    coord, max_area = max(area, key=itemgetter(1))

    return max_area


def solve_b(data):
    coords = process_data(data)
    max_x, max_y, min_x, min_y = area_bounds(coords)
    area_map = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distance = sum(manhattan_distance(coord, (x, y)) for coord in coords)
            if distance < 10000:
                area_map[x, y] = 1
    return sum(area_map.values())
