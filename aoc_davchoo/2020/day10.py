from more_itertools import pairwise
from collections import Counter


def process_data(data):
    return [int(rating) for rating in data.splitlines()]


def solve_a(data):
    adapters = process_data(data)
    adapters.append(0)  # Charging outlet
    adapters.append(max(adapters) + 3)  # Built in adapter
    adapters.sort()

    differences = [b - a for a, b in pairwise(adapters)]
    difference_counts = Counter(differences)
    return difference_counts[1] * difference_counts[3]


def solve_b(data):
    adapters = process_data(data)
    adapters.append(0)  # Charging outlet
    adapters.sort()

    cached_combos = {}

    def dfs(current_adaptor):
        if current_adaptor == 0:
            return 0
        elif current_adaptor in cached_combos.keys():
            return cached_combos[current_adaptor]

        combos = 0
        for i in [1, 2, 3]:
            if (current_adaptor - i) in adapters:
                combos += dfs(current_adaptor - i) + 1
        combos -= 1
        cached_combos[current_adaptor] = combos
        return combos

    return dfs(max(adapters) + 3) + 1
