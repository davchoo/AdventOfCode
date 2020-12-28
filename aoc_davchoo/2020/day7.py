import re


def process_data(data):
    outer_bag_regex = re.compile(r"^(.+?)\sbags")
    inner_bags_regex = re.compile(r"(\d+)\s(.+?)\sbag")

    rules = {}

    for rule in data.splitlines():
        outer_bag = outer_bag_regex.findall(rule)[0]
        inner_bags = inner_bags_regex.findall(rule)

        rules[outer_bag] = {color: int(quantity) for quantity, color in inner_bags}

    return rules


def reverse_rules(rules):
    mapping = {}
    for outer_bag, inner_bags in rules.items():
        for inner_bag in inner_bags.keys():
            if inner_bag not in mapping.keys():
                mapping[inner_bag] = [outer_bag]
            else:
                mapping[inner_bag].append(outer_bag)
    return mapping


def solve_a(data):
    rules = process_data(data)
    mapping = reverse_rules(rules)
    valid_bags = set()

    def dfs(inner_bag):
        if inner_bag not in mapping.keys():
            return
        for outer_bag in mapping[inner_bag]:
            if outer_bag not in valid_bags:
                valid_bags.add(outer_bag)
                dfs(outer_bag)

    dfs("shiny gold")

    return len(valid_bags)


def solve_b(data):
    rules = process_data(data)

    def dfs(outer_bag):
        total = sum(quantity * (dfs(inner_bag) + 1) for inner_bag, quantity in rules[outer_bag].items())
        return total

    return dfs("shiny gold")
