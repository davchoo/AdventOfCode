from collections import Counter, defaultdict


def process_data(data):
    scan = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            scan[x, y] = char
    return scan


def calculate_biodiversity(scan):
    biodiversity_rating = 0

    for (x, y), state in scan.items():
        if state == "#":
            tile_number = 5 * y + x
            biodiversity_rating += pow(2, tile_number)

    return biodiversity_rating


def bug_iteration(scan, find_adjacent):
    count = {pos: Counter(find_adjacent(*pos)) for pos in scan.keys()}
    for pos, counts in count.items():
        if scan[pos] == ".":
            if counts["#"] == 1 or counts["#"] == 2:
                scan[pos] = "#"
        else:
            if counts["#"] != 1:
                scan[pos] = "."
    return scan


adjacent_offsets = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]


def solve_a(data):
    scan = process_data(data)

    previous_scans = []

    def find_adjacent(x, y):
        for offset_x, offset_y in adjacent_offsets:
            new_x = x + offset_x
            new_y = y + offset_y
            yield scan.get((new_x, new_y), ".")

    while scan not in previous_scans:
        previous_scans.append(scan.copy())
        scan = bug_iteration(scan, find_adjacent)

    return calculate_biodiversity(scan)


def solve_b(data):
    base_level_scan = process_data(data)

    scan = defaultdict(lambda: ".")

    for (x, y), state in base_level_scan.items():
        if x == 2 and y == 2:
            continue
        scan[x, y, 0] = state

    def get_adjacent_pos(x, y, level):
        inner_recursion_adjacent = {
            (2, 1): [(i, 0) for i in range(5)],  # N
            (3, 2): [(4, i) for i in range(5)],  # E
            (2, 3): [(i, 4) for i in range(5)],  # S
            (1, 2): [(0, i) for i in range(5)]   # W
        }

        outer_recursion_adjacent = {}
        for i in range(5):
            outer_recursion_adjacent[i, -1] = (2, 1)  # N
            outer_recursion_adjacent[5, i] = (3, 2)   # E
            outer_recursion_adjacent[i, 5] = (2, 3)   # S
            outer_recursion_adjacent[-1, i] = (1, 2)  # W

        for offset_x, offset_y in adjacent_offsets:
            new_x = x + offset_x
            new_y = y + offset_y
            if new_x == 2 and new_y == 2:
                for inner_x, inner_y in inner_recursion_adjacent[x, y]:
                    yield inner_x, inner_y, level + 1
            elif (new_x, new_y) in outer_recursion_adjacent:
                new_x, new_y = outer_recursion_adjacent[new_x, new_y]
                yield new_x, new_y, level - 1
            else:
                yield new_x, new_y, level

    def find_adjacent(x, y, level):
        for adj_x, adj_y, adj_level in get_adjacent_pos(x, y, level):
            yield scan.get((adj_x, adj_y, adj_level), ".")

    for i in range(200):
        # Initialize spaces adjacent to bugs
        for pos, state in scan.copy().items():
            if state == "#":
                for adj_pos in get_adjacent_pos(*pos):
                    if adj_pos not in scan:
                        scan[adj_pos] = "."

        bug_iteration(scan, find_adjacent)

    return Counter(scan.values())["#"]
