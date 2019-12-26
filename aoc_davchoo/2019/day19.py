from collections import defaultdict
from itertools import count

from .intcode import load_program, IntCodeMachine


def test_location(program, x, y):
    machine = IntCodeMachine(program, [x, y])
    machine.return_output = True
    pulled = machine.run()
    return pulled


def solve_a(data):
    program = load_program(data)

    pulled_map = {}

    for y in range(50):
        for x in range(50):
            pulled_map[x, y] = test_location(program, x, y)

    return sum(pulled_map.values())


def solve_b(data):
    program = load_program(data)

    pulled_map = defaultdict(int)

    x = 0
    y = 0
    while True:
        # Count x till we reach a pulling spot
        for i, x in enumerate(count(x)):
            pulled_map[x, y] = test_location(program, x, y)
            if pulled_map[x, y] == 1:
                break
            if i > 50:  # First few lines are too narrow
                break
        if i > 50:
            # Reset to the start
            x = 0
        else:
            # Test the top right corner of a 100x100 square
            if (y - 99) >= 0:
                pulled = test_location(program, x + 99, y - 99)
                if pulled == 1:
                    return x * 10000 + (y - 99)
        y += 1
