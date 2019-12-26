import string
from collections import deque, defaultdict
from itertools import groupby
from operator import itemgetter

from more_itertools import first_true


def find_adjacent(pos, maze: dict):
    x, y = pos
    adjacent_offset = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    adjacent = []
    for offset_x, offset_y in adjacent_offset:
        adj_x = x + offset_x
        adj_y = y + offset_y
        if (adj_x, adj_y) in maze:
            adjacent.append(((adj_x, adj_y), maze[adj_x, adj_y]))

    return adjacent


def process_data(data):
    maze = dict()
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            maze[x, y] = char

    portals = [pos for pos, char in maze.items() if char in string.ascii_letters]

    for pos in portals:
        adjacent = find_adjacent(pos, maze)
        # If letter is next to open space
        if any(char == "." for adj_pos, char in adjacent):
            letter = maze[pos]
            other_letter_pos, other_letter = first_true(adjacent, pred=lambda char: char[1] in string.ascii_letters)
            offset_x = other_letter_pos[0] - pos[0]
            offset_y = other_letter_pos[1] - pos[1]
            portal_name = ""
            if offset_x == 0 and offset_y == -1:  # Up Down
                portal_name = other_letter + letter
            elif offset_x == 1 and offset_y == 0:  # Left Right
                portal_name = letter + other_letter
            elif offset_x == 0 and offset_y == 1:  # Up Down
                portal_name = letter + other_letter
            elif offset_x == -1 and offset_y == 0:  # Left Right
                portal_name = other_letter + letter
            maze[pos] = portal_name

    # Remove letters adjacent to portals
    for pos in portals:
        if len(maze[pos]) == 1 and maze[pos] in string.ascii_letters:
            maze[pos] = " "

    portals = [(maze[pos], pos) for pos in portals if len(maze[pos]) == 2]
    portals.sort(key=itemgetter(0))

    grouped_portals = {}
    for portal_name, positions in groupby(portals, itemgetter(0)):
        grouped_portals[portal_name] = [pos for name, pos in positions]

    return maze, grouped_portals


def pathfind_normal(maze, portals, start_pos, end_pos):
    maze_map = {}
    open_locations = [(start_pos, 0)]  # (Pos, distance)
    closed_locations = set()

    while len(open_locations) > 0:
        open_locations.sort(key=itemgetter(1))
        current_pos, current_distance = open_locations.pop(0)
        current_location = maze[current_pos]

        if current_pos in maze_map and current_distance > maze_map[current_pos]:
            continue

        maze_map[current_pos] = current_distance
        closed_locations.add(current_pos)
        if current_location == ".":
            new_distance = current_distance + 1
            for pos, char in find_adjacent(current_pos, maze):
                if char != "#" and char != "AA":
                    if pos not in closed_locations:
                        open_locations.append((pos, new_distance))
                    elif maze_map.get(pos, -1) > new_distance:
                        open_locations.append((pos, new_distance))
        else:  # We're on a portal
            if current_location == "AA" or current_location == "ZZ":
                continue
            portal_pair = portals[current_location]
            other_portal_pos = (set(portal_pair) - {current_pos}).pop()
            closed_locations.add(other_portal_pos)

            adjacent_portal = first_true(find_adjacent(other_portal_pos, maze), pred=lambda x: x[1] == ".")[0]
            open_locations.append((adjacent_portal, current_distance))

    return maze_map[end_pos]


def pathfind_recursive(maze, portals, start_pos, end_pos):
    width = max(maze.keys(), key=itemgetter(0))[0]
    height = max(maze.keys(), key=itemgetter(1))[1]

    maze_map = defaultdict(lambda: dict())
    open_locations = [(start_pos, 0, 0)]  # (Pos, level, distance)
    closed_locations = set()

    while len(open_locations) > 0:
        open_locations.sort(key=itemgetter(1))
        current_pos, current_level, current_distance = open_locations.pop(0)
        current_location = maze[current_pos]

        # We got to the exit in level 0 and it has the minimum distance
        if (end_pos, 0) in closed_locations and maze_map[0][end_pos] > current_distance:
            break

        if current_pos in maze_map[current_level] and current_distance > maze_map[current_pos]:
            continue

        maze_map[current_level][current_pos] = current_distance
        closed_locations.add((current_pos, current_level))
        if current_location == ".":
            new_distance = current_distance + 1
            for pos, char in find_adjacent(current_pos, maze):
                if char != "#" and char != "AA":
                    if (pos, current_level) not in closed_locations:
                        open_locations.append((pos, current_level, new_distance))
                    elif maze_map[current_level].get(pos, -1) > new_distance:
                        open_locations.append((pos, current_level, new_distance))
        else:  # We're on a portal
            if current_location == "AA" or current_location == "ZZ":
                continue

            # Inner or Outer portal
            x, y = current_pos
            inner_portal = True
            if x == 1 or y == 1 or x == (width - 1) or y == (height - 1):
                inner_portal = False

            new_level = current_level + 1
            if not inner_portal:
                # Outer portals on level 0 are closed
                if current_level == 0:
                    continue
                new_level = current_level - 1

            portal_pair = portals[current_location]
            other_portal_pos = (set(portal_pair) - {current_pos}).pop()

            closed_locations.add((other_portal_pos, new_level))

            adjacent_portal = first_true(find_adjacent(other_portal_pos, maze), pred=lambda x: x[1] == ".")[0]
            open_locations.append((adjacent_portal, new_level, current_distance))

    return maze_map[0][end_pos]


def find_start_and_end(maze: dict, portals):
    entrance_portal = portals["AA"][0]
    exit_portal = portals["ZZ"][0]

    start_pos = first_true(find_adjacent(entrance_portal, maze), pred=lambda x: x[1] == ".")[0]
    end_pos = first_true(find_adjacent(exit_portal, maze), pred=lambda x: x[1] == ".")[0]

    return start_pos, end_pos


def solve_a(data):
    maze, portals = process_data(data)
    start_pos, end_pos = find_start_and_end(maze, portals)
    return pathfind_normal(maze, portals, start_pos, end_pos)


def solve_b(data):
    maze, portals = process_data(data)
    start_pos, end_pos = find_start_and_end(maze, portals)
    return pathfind_recursive(maze, portals, start_pos, end_pos)