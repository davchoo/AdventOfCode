from importlib import import_module
from argparse import ArgumentParser
from aocd.models import Puzzle
from time import perf_counter
from sys import exc_info, exit
from os import environ
from pathlib import Path
import json
from datetime import date


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
    parser.add_argument("--token")
    parser.add_argument("--user")

    args = parser.parse_args()

    if args.token is not None:
        environ["AOC_SESSION"] = args.token

    if args.user is not None:
        token_file = Path.home().joinpath(".config/aocd/tokens.json")
        if token_file.exists() and token_file.is_file():
            with token_file.open("r") as file:
                token_json = json.loads(file.read())
                if args.user in token_json:
                    environ["AOC_SESSION"] = token_json[args.user]
                else:
                    print(f"User {args.user} does not exist in tokens.json")
                    exit(-1)
        else:
            print("~/.config/aocd/tokens.json doesn't exist")
            exit(-2)

    today = date.today()

    if args.days is None:
        if args.year == today.year:
            args.days = range(1, today.day + 1)

    for day in args.days:
        if day < 0 or day > 25 or (args.year == today.year and day > today.day):
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
            raise exc_info()[1]
