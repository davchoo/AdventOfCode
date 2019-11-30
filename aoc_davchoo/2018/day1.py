import itertools


def solve_a(data):
    frequency_deltas = list(map(int, data.split()))
    final_frequency = sum(frequency_deltas)
    return final_frequency


def solve_b(data):
    frequency_deltas = list(map(int, data.split()))
    previous_frequencies = set()
    current_frequency = 0
    for delta in itertools.cycle(frequency_deltas):
        current_frequency += delta
        if current_frequency in previous_frequencies:
            return current_frequency
        previous_frequencies.add(current_frequency)
    return -1
