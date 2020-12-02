import re


def process_data(data):
    regex = re.compile(r"(\d+)-(\d+) (\w):\s(\w+)")
    data = [regex.findall(line)[0] for line in data.splitlines()]
    return [((int(entry[0]), int(entry[1]), entry[2]), entry[3]) for entry in data]


def verify_password_a(policy, password: str):
    min_instance, max_instance, letter = policy
    return min_instance <= password.count(letter) <= max_instance


def solve_a(data):
    entries = process_data(data)
    valid = [verify_password_a(*entry) for entry in entries]
    return valid.count(True)


def verify_password_b(policy, password: str):
    index_a, index_b, letter = policy
    return (password[index_a - 1] == letter) != (password[index_b - 1] == letter)


def solve_b(data):
    entries = process_data(data)
    valid = [verify_password_b(*entry) for entry in entries]
    return valid.count(True)
