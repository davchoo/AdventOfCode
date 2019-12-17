from collections import deque

from more_itertools import first_true

from .intcode import load_program, IntCodeMachine
from copy import deepcopy

direction_offset = {
    "N": (1, (0, -1)),
    "S": (2, (0, 1)),
    "W": (3, (-1, 0)),
    "E": (4, (1, 0))
}


def map_out_area(machine: IntCodeMachine):
    machine.run()

    area_map = {(0, 0): (0, 1)}  # Pos: (Distance, Status)
    open_locations = deque([((0, 0), 0, machine)])  # (Pos, Distance, Machine)
    locations = {(0, 0)}

    while len(open_locations) > 0:
        pos, distance, machine = open_locations.pop()
        status = machine.run()
        if status is not None:
            area_map[pos] = (distance, status)
            if status == 0:
                continue

        for direction, (command, offset) in direction_offset.items():
            new_position = (pos[0] + offset[0], pos[1] + offset[1])
            if new_position not in locations:
                new_machine: IntCodeMachine = deepcopy(machine)
                new_machine.set_input(command)

                open_locations.append((new_position, distance + 1, new_machine))
                locations.add(new_position)

    return area_map


def create_oxygen_map(area_map):
    # Reset distance data
    for pos, (distance, status) in area_map.items():
        area_map[pos] = (-1, status)

    oxygen_system_pos = first_true(area_map.items(), pred=lambda x: x[1][1] == 2)[0]
    open_locations = deque([(oxygen_system_pos, 0)]) # (Pos, Distance)
    locations = {oxygen_system_pos}

    while len(open_locations) > 0:
        pos, distance = open_locations.popleft()
        _, status = area_map[pos]
        area_map[pos] = (distance, status)

        for direction, (command, offset) in direction_offset.items():
            new_position = (pos[0] + offset[0], pos[1] + offset[1])
            if new_position not in locations:
                locations.add(new_position)
                if area_map[new_position][1] == 1:
                    open_locations.append((new_position, distance + 1))

    return area_map


def create_map(data):
    program = load_program(data)
    machine = IntCodeMachine(program)
    machine.return_output = True

    area_map = map_out_area(machine)
    return area_map


def solve_a(data):
    area_map = create_map(data)
    oxygen_system = first_true(area_map.items(), pred=lambda x: x[1][1] == 2)
    return oxygen_system[1][0]


def solve_b(data):
    area_map = create_map(data)
    area_map = create_oxygen_map(area_map)
    farthest_location = max(area_map.items(), key=lambda x: x[1][0])
    return farthest_location[1][0]
