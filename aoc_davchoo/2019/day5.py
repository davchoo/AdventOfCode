from .intcode import run_program, load_program


def solve_a(data):
    program = load_program(data)
    memory, output = run_program(program, [1])
    assert all(code == 0 for code in output[:-1])
    return output[-1]


def solve_b(data):
    program = load_program(data)
    memory, output = run_program(program, [5])
    return output[0]
