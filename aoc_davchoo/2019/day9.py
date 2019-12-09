from .intcode import load_program, run_program


def solve_a(data):
    program = load_program(data)
    memory, output = run_program(program, [1])
    return output[0]


def solve_b(data):
    program = load_program(data)
    memory, output = run_program(program, [2])
    return output[0]
