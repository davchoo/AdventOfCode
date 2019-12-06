from .intcode import run_program


def process_data(data):
    program = list(map(int, data.split(",")))
    return program


def solve_a(data):
    program = process_data(data)
    memory, output = run_program(program, [1])
    assert all(code == 0 for code in output[:-1])
    return output[-1]


def solve_b(data):
    program = process_data(data)
    memory, output = run_program(program, [5])
    return output[0]
