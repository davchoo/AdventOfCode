import collections
from operator import itemgetter
import re
import string


def process_data(data: str):
    depend_pairs = data.splitlines()
    regex = re.compile(r" (\w) ")
    depend_pairs = list(map(regex.findall, depend_pairs))
    dependencies = collections.defaultdict(list)
    #  Fill with empty lists
    steps, depends = zip(*depend_pairs)
    all_steps = set(steps).union(set(depends))
    for step in all_steps:
        dependencies[step] = []

    for depend, step in depend_pairs:
        dependencies[step].append(depend)
    return all_steps, dependencies


def get_next_steps(dependencies):
    free_steps = map(itemgetter(0), filter(lambda x: len(x[1]) == 0, dependencies.items()))
    return list(sorted(free_steps, reverse=True))


def solve_a(data):
    all_steps, dependencies = process_data(data)
    instructions = []

    next_steps = get_next_steps(dependencies)
    while len(next_steps) > 0:
        next_step = next_steps.pop()
        instructions.append(next_step)
        del dependencies[next_step]
        for step, depends in dependencies.items():
            dependencies[step] = list(filter(lambda x: x != next_step, depends))
        next_steps = get_next_steps(dependencies)

    return "".join(instructions)


def solve_b(data):
    all_steps, dependencies = process_data(data)

    time_taken = 0
    workers = [[".", 0], [".", 0], [".", 0], [".", 0], [".", 0]]
    while len(dependencies) > 0:
        # Filter out completed steps
        for worker in workers:
            letter, time = worker
            if time == 0 and letter != ".":
                for step, depends in dependencies.items():
                    dependencies[step] = list(filter(lambda x: x != letter, depends))
        # Assign new tasks
        next_steps = get_next_steps(dependencies)
        for worker in workers:
            letter, time = worker
            if time == 0:
                if len(next_steps) > 0:
                    next_step = next_steps.pop()
                    del dependencies[next_step]
                    time_remaining = string.ascii_uppercase.index(next_step) + 61
                    worker[0] = next_step
                    worker[1] = time_remaining
                else:
                    worker[0] = "."
                    worker[1] = 0
        # Take a time step equal to the minimum remaining time
        in_queue, times = zip(*workers)
        time_step = min(filter(lambda x: x > 0, times))
        time_taken += time_step
        for worker in workers:
            if worker[1] == 0:
                continue
            worker[1] -= time_step
    return time_taken
