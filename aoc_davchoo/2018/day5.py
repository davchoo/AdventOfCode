from more_itertools import sliced
import string


def reacts(a, b):
    # Pair is the same letter
    if a.lower() == b.lower():
        # One is uppercase and another is lowercase
        if a != b:
            return True
    return False


def reduce_polymer(polymer):
    for a in range(len(polymer) - 1):
        if polymer[a] is None:
            continue

        if reacts(polymer[a], polymer[a + 1]):
            polymer[a] = None
            polymer[a + 1] = None
    return list(filter(lambda x: x is not None, polymer))


def fully_reduce(polymer):
    current_polymer = list(polymer)
    new_polymer = reduce_polymer(current_polymer)
    while new_polymer != current_polymer:
        current_polymer = new_polymer
        new_polymer = reduce_polymer(current_polymer)
    return current_polymer


def solve_a(data):
    return len(fully_reduce(data))


def solve_b(data):
    smallest_polymer = len(fully_reduce(data))
    for unit in string.ascii_lowercase:
        new_polymer = filter(lambda x: x.lower() != unit, data)
        reduced_polymer = fully_reduce(new_polymer)
        smallest_polymer = min(len(reduced_polymer), smallest_polymer)
    return smallest_polymer
