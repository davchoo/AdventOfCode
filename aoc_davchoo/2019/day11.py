from collections import defaultdict
from operator import itemgetter

import numpy as np
from PIL import Image

from .intcode import load_program, run_with_state, IntCodeState


def run_robot(hull, program):
    direction_offsets = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0)
    }

    state = IntCodeState(program)
    state.wait_on_output = True
    run_with_state(state)

    robot_x = 0
    robot_y = 0
    robot_direction = 0
    num_colored = 0

    while not state.halt:
        if (robot_x, robot_y) not in hull:
            num_colored += 1  # Going to paint a new panel
        current_color = hull[robot_x, robot_y]
        state.set_input([current_color])
        run_with_state(state)
        if state.halt:
            num_colored -= 1  # Didn't paint it yet
            break

        new_color = state.output[-1]
        hull[robot_x, robot_y] = new_color
        state.waiting_io = False
        run_with_state(state)
        if state.halt:
            break

        turn = state.output[-1]
        if turn == 0:
            robot_direction -= 1
        else:
            robot_direction += 1

        if robot_direction < 0:
            robot_direction = 3
        elif robot_direction > 3:
            robot_direction = 0
        offset_x, offset_y = direction_offsets[robot_direction]
        robot_x += offset_x
        robot_y += offset_y
    return num_colored


def solve_a(data):
    program = load_program(data)
    hull = defaultdict(lambda: 0)
    num_colored = run_robot(hull, program)
    return num_colored


def solve_b(data):
    program = load_program(data)
    hull = defaultdict(lambda: 0)
    hull[0, 0] = 1
    num_colored = run_robot(hull, program)

    min_x = min(hull.keys(), key=itemgetter(0))[0]
    min_y = min(hull.keys(), key=itemgetter(1))[1]
    max_x = max(hull.keys(), key=itemgetter(0))[0]
    max_y = max(hull.keys(), key=itemgetter(1))[1]
    final_image = np.zeros((max_y - min_y + 1, max_x - min_x + 1, 3), dtype=np.uint8)
    color_palette = [[0, 0, 0], [255, 255, 255]]
    for img_x, hull_x in enumerate(range(min_x, max_x + 1)):
        for img_y, hull_y in enumerate(range(min_y, max_y + 1)):
            final_image[img_y, img_x] = color_palette[hull[hull_x, hull_y]]
    img = Image.fromarray(final_image, 'RGB')
    img.save('day11.png')

    return 0
