from itertools import combinations


def process_data(data):
    return [int(line) for line in data.splitlines()]


def verify(previous_numbers, number):
    for a, b in combinations(previous_numbers, 2):
        if (a + b) == number:
            return True
    return False


def find_invalid(data):
    for i, number in enumerate(data):
        if i < 25:
            continue
        if not verify(data[i-25:i], number):
            return number
    return None


def solve_a(data):
    data = process_data(data)
    return find_invalid(data)


def solve_b(data):
    data = process_data(data)
    invalid_number = find_invalid(data)
    for i, a in enumerate(data):
        running_sum = a
        for j, b in enumerate(data[i+1:], start=i+1):
            running_sum += b
            if running_sum == invalid_number:
                smallest_number = min(data[i:j+1])
                largest_number = max(data[i:j+1])
                return smallest_number + largest_number
            elif running_sum > invalid_number:
                break
    return None
