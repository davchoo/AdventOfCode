from collections import defaultdict
import math
import re


def process_data(data):
    reactions = {}
    for line in data.splitlines():
        chemicals = []
        for chemical in re.findall(r"(\d+ \w+)", line):
            quantity, name = chemical.split(" ")
            chemicals.append((int(quantity), name))
        *reactants, result = chemicals
        reactions[result[1]] = (result[0], reactants)
    return reactions


def process_requirements(amount_required: int, chemical: str, reactions: dict, surplus_chemicals=None):
    if surplus_chemicals is None:
        surplus_chemicals = defaultdict(int)
    if chemical == "ORE":
        return amount_required

    if surplus_chemicals[chemical] != 0:
        surplus_used = min(amount_required, surplus_chemicals[chemical])
        amount_required -= surplus_used
        surplus_chemicals[chemical] -= surplus_used

    amount_produced, reactants = reactions[chemical]
    multiple = math.ceil(amount_required / amount_produced)
    surplus = (multiple * amount_produced) - amount_required
    surplus_chemicals[chemical] += surplus

    ore_required = 0

    for reactant_amount, reactant_name in reactants:
        ore_required += process_requirements(reactant_amount * multiple, reactant_name, reactions, surplus_chemicals)

    return ore_required


def solve_a(data):
    reactions = process_data(data)
    ore_required = process_requirements(1, "FUEL", reactions)
    return ore_required


def solve_b(data):
    reactions = process_data(data)
    ore = 1000000000000
    # Lower limit is (units of ore) / (units of ore for 1 fuel)
    lower_limit = ore // process_requirements(1, "FUEL", reactions)
    # Increase fuel produced till ore requirements exceed the units of ore we have
    upper_limit = 0
    steps = 100000
    for i in range(lower_limit, ore, steps):
        ore_required = process_requirements(i, "FUEL", reactions)
        if ore_required >= ore:
            upper_limit = i
            break
    # Binary search for the max fuel we can produce
    while True:
        if (upper_limit - lower_limit) == 1:
            return lower_limit
        fuel_produced = (upper_limit + lower_limit) // 2
        ore_required = process_requirements(fuel_produced, "FUEL", reactions)
        if ore_required > ore:
            upper_limit = fuel_produced
        else:
            lower_limit = fuel_produced
