from collections import Counter

from more_itertools import chunked

from .intcode import load_program, run_program, run_with_state, IntCodeState


def solve_a(data):
    program = load_program(data)
    memory, output = run_program(program, [])
    screen = {}
    for (x, y, id) in chunked(output, 3):
        screen[x, y] = id
    return Counter(screen.values())[2]


def solve_b(data):
    program = load_program(data)
    program[0] = 2
    state = IntCodeState(program)
    state.wait_on_output = True

    screen = {}
    score = 0
    state.set_input([0])
    while not state.halt:
        # Draw till another joystick input is requested
        while True:
            state.waiting_io = False
            run_with_state(state)
            state.waiting_io = False
            run_with_state(state)
            state.waiting_io = False
            run_with_state(state)
            if state.halt or state.io_direction == "Read":
                break
            x, y, id = state.output[-3:]
            if x == -1 and y == 0:
                score = id
            else:
                screen[x, y] = id

        if not state.halt:
            paddle = [pos for pos, id in screen.items() if id == 3][0]
            ball = [pos for pos, id in screen.items() if id == 4][0]
            # Keep paddle under ball
            if ball[0] > paddle[0]:
                state.set_input([1])
            elif ball[0] < paddle[0]:
                state.set_input([-1])
            else:
                state.set_input([0])
            print(paddle, ball)

    assert Counter(screen.values())[2] == 0
    return score
