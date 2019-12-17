from collections import Counter

from more_itertools import chunked

from .intcode import load_program, run_program, IntCodeMachine


def solve_a(data):
    program = load_program(data)
    memory, output = run_program(program, [])
    screen = {}
    for (x, y, tile) in chunked(output, 3):
        screen[x, y] = tile
    return Counter(screen.values())[2]


def solve_b(data):
    program = load_program(data)
    program[0] = 2
    machine = IntCodeMachine(program)
    machine.return_output = True

    screen = {}
    score = 0
    machine.set_input(0)
    while not machine.halt:
        # Draw till another joystick input is requested
        while True:
            x = machine.run()
            y = machine.run()
            tile = machine.run()
            if machine.halt or machine.waiting_input:
                break
            if x == -1 and y == 0:
                score = tile
            else:
                screen[x, y] = tile

        if not machine.halt:
            paddle = [pos for pos, tile in screen.items() if tile == 3][0]
            ball = [pos for pos, tile in screen.items() if tile == 4][0]
            # Keep paddle under ball
            if ball[0] > paddle[0]:
                machine.set_input(1)
            elif ball[0] < paddle[0]:
                machine.set_input(-1)
            else:
                machine.set_input(0)

    assert Counter(screen.values())[2] == 0
    return score
