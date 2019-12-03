def layout_wire(wire):
    wire_map = {}
    current_location = (0, 0)
    steps = 1
    for direction, length in wire:
        char, offset = directions_map[direction]
        for i in range(length):
            current_location = tuple(sum(x) for x in zip(current_location, offset))
            wire_map[current_location] = (char, steps)
            steps += 1
        wire_map[current_location] = ("+", steps - 1)
    return wire_map


def process_data(data):
    wire_paths = data.splitlines()
    wire_paths = [[(step[0], int(step[1::])) for step in wire.split(",")] for wire in wire_paths]
    return [layout_wire(wire) for wire in wire_paths]


directions_map = {
    "L": ("-", (-1, 0)),
    "U": ("|", (0, -1)),
    "R": ("-", (1, 0)),
    "D": ("|", (0, 1)),
}


def manhattan_distance(coord1, coord2=(0, 0)):
    return abs(coord2[0] - coord1[0]) + abs(coord2[1] - coord1[1])


def solve_a(data):
    wires = process_data(data)
    intersections = set(wires[0].keys()) & set(wires[1].keys())
    intersection_distances = [manhattan_distance(pos) for pos in intersections]
    closest_intersection = min(intersection_distances)
    return closest_intersection


def solve_b(data):
    wires = process_data(data)
    intersections = set(wires[0].keys()) & set(wires[1].keys())
    intersection_distances = [wires[0][pos][1] + wires[1][pos][1] for pos in intersections]
    closest_intersection = min(intersection_distances)
    return closest_intersection
