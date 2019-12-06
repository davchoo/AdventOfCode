from .intcode import run_program


def process_data(data):
    program = list(map(int, data.split(",")))
    return program


def solve_a(data):
    program = process_data(data)

    program[1] = 12
    program[2] = 2
    memory, output = run_program(program)
    return memory[0]


def solve_b(data):
    program = process_data(data)
    for noun in range(100):
        for verb in range(100):
            program[1] = noun
            program[2] = verb

            memory, output = run_program(program)
            if memory[0] == 19690720:
                return 100 * noun + verb
    return -1
