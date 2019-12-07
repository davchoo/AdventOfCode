from .intcode import run_program, load_program


def solve_a(data):
    program = load_program(data)

    program[1] = 12
    program[2] = 2
    memory, output = run_program(program)
    return memory[0]


def solve_b(data):
    program = load_program(data)
    for noun in range(100):
        for verb in range(100):
            program[1] = noun
            program[2] = verb

            memory, output = run_program(program)
            if memory[0] == 19690720:
                return 100 * noun + verb
    return -1
