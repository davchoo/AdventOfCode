from itertools import combinations
from functools import reduce
import operator


def process_data(data):
    expenses = [int(expense) for expense in data.splitlines()]
    return expenses


def find_answer(expenses, num_entries):
    for entries in combinations(expenses, num_entries):
        if sum(entries) == 2020:
            return reduce(operator.mul, entries)


def solve_a(data):
    expenses = process_data(data)
    return find_answer(expenses, 2)


def solve_b(data):
    expenses = process_data(data)
    return find_answer(expenses, 3)
