from more_itertools import pairwise, run_length, ilen


def process_data(data):
    min_password, max_password = map(int, data.split("-"))
    return min_password, max_password


def is_password_valid(password, min_password, max_password):
    # Password is 6 digits
    if min_password <= password <= max_password:
        digits = str(password)
        # Password has no decreasing pairs
        for a, b in pairwise(digits):
            if a > b:
                return False
        # Password has at least one pair of equal digits
        for a, b in pairwise(digits):
            if a == b:
                break
        else:
            return False
        return True
    return False


def solve_a(data):
    min_password, max_password = process_data(data)
    valid_passwords = 0
    for i in range(min_password, max_password + 1):
        if is_password_valid(i, min_password, max_password):
            valid_passwords += 1
    return valid_passwords


def fits_part_b_constraint(password):
    digits = str(password)
    groups = run_length.encode(digits)
    larger_groups = [digit if size > 2 else None for digit, size in groups]
    adjacent_pairs = filter(lambda pair: pair[0] == pair[1], pairwise(digits))
    valid_pairs = filter(lambda pair: pair[0] not in larger_groups, adjacent_pairs)
    return ilen(valid_pairs) > 0


def solve_b(data):
    min_password, max_password = process_data(data)
    valid_passwords = 0
    for i in range(min_password, max_password + 1):
        if is_password_valid(i, min_password, max_password):
            if fits_part_b_constraint(i):
                valid_passwords += 1
    return valid_passwords
