import collections
import itertools


def solve_a(data):
    box_ids = data.split()
    pair_counts = 0
    triple_counts = 0

    for box_id in box_ids:
        letter_counts = collections.Counter(box_id)
        if 2 in letter_counts.values():
            pair_counts += 1
        if 3 in letter_counts.values():
            triple_counts += 1

    return pair_counts * triple_counts


def solve_b(data):
    box_ids = data.split()
    for a, b in itertools.product(box_ids, box_ids):
        if a == b:
            continue
        compare = [letter_a == letter_b for letter_a, letter_b in zip(a, b)]
        if compare.count(False) == 1:
            return "".join(itertools.compress(a, compare))
    return "Failed"
