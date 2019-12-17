from .intcode import run_program, IntCodeMachine, load_program
from more_itertools import distinct_permutations
from itertools import cycle


def solve_a(data):
    program = load_program(data)
    max_signal = -1e1000
    for phases in distinct_permutations(range(5)):
        input_signal = 0
        for phase in phases:
            memory, output = run_program(program, [phase, input_signal])
            input_signal = output[0]
        max_signal = max(max_signal, input_signal)
    return max_signal


def solve_b(data):
    program = load_program(data)
    max_signal = -1e1000
    for phases in distinct_permutations(range(5, 10)):
        machines = [IntCodeMachine(program) for _ in range(5)]
        # Give phase input to all amplifiers
        for phase, machine in zip(phases, machines):
            machine.set_input(phase)
            machine.return_output = True
            machine.run()

        # Pass the output of each amplifier to the next one in a loop
        input_signal = 0
        for machine in cycle(machines):
            machine.set_input(input_signal)
            input_signal = machine.run() or input_signal
            if machine.halt:
                break
        max_signal = max(max_signal, input_signal)
    return max_signal
