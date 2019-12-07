from .intcode import run_program, run_with_state, IntCodeState, load_program
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
        program_states = [IntCodeState(program) for _ in range(5)]
        # Give phase input to all amplifiers
        for phase, state in zip(phases, program_states):
            state.set_input([phase])
            state.wait_on_output = True
            run_with_state(state)

        # Pass the output of each amplifier to the next one in a loop
        input_signal = [0]
        for state in cycle(program_states):
            state.waiting_io = False
            state.set_input(input_signal)
            run_with_state(state)
            if state.waiting_io:
                input_signal = state.output
                state.output = []
            elif state.halt:
                break
        max_signal = max(max_signal, input_signal[0])
    return max_signal
