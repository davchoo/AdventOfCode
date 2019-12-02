from .intcode import run_program


def process_data(data):
    program = list(map(int, data.split(",")))
    return program


def solve_a(data):
    program = process_data(data)

    program[1] = 12
    program[2] = 2
    result, memory = run_program(program)
    return result


def solve_b(data):
    program = process_data(data)
    for noun in range(100):
        for verb in range(100):
            new_program = program[::]
            new_program[1] = noun
            new_program[2] = verb

            result, memory = run_program(new_program)
            if result == 19690720:
                return 100 * noun + verb
    return -1
