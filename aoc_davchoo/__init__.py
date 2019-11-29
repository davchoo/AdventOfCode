from importlib import import_module
from argparse import ArgumentParser
from aocd.models import Puzzle
from time import perf_counter
from sys import exc_info


def solve(year, day, data):
    mod_name = f"aoc_davchoo.{year}.day{day}"
    mod = import_module(mod_name)
    a = mod.solve_a(data)
    b = mod.solve_b(data)
    return a, b


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--days", nargs="+", action="extend", type=int)

    args = parser.parse_args()
    if args.days is None:
        args.days = range(1, 26)

    for day in args.days:
        if day < 0 or day > 25:
            print(f"Invalid Day {day}")
            continue
        puzzle = Puzzle(args.year, day)
        try:
            start_time = perf_counter()
            part_a, part_b = solve(args.year, day, puzzle.input_data)
            end_time = perf_counter()
            elasped_time = end_time - start_time
            print(f"{elasped_time:.2f}s {args.year}/{day} - {puzzle.title} Part A: {part_a}   Part B: {part_b}")
        except:
            print(f"      {args.year}/{day} - {puzzle.title} - {exc_info()[1]}")
