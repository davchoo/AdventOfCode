from itertools import chain


def solve_a(data):
    groups = data.split("\n\n")
    return sum(len(set(chain(*group.splitlines()))) for group in groups)


def solve_b(data):
    sum_yes = 0
    groups = data.split("\n\n")
    for group in groups:
        group = group.splitlines()
        yes_answers = set(group[0])
        for person in group:
            yes_answers.intersection_update(person)
        sum_yes += len(yes_answers)
    return sum_yes
