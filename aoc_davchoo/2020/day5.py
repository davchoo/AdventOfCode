def bits_to_int(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out


def get_seat(bsp):
    row = bits_to_int({"F": 0, "B": 1}[char] for char in bsp[:7])
    col = bits_to_int({"L": 0, "R": 1}[char] for char in bsp[7:])

    return row, col


def get_seat_id(row, col):
    return row * 8 + col


def process_data(data):
    return [get_seat_id(*get_seat(bsp)) for bsp in data.splitlines()]


def solve_a(data):
    seat_ids = process_data(data)
    return max(seat_ids)


def solve_b(data):
    seat_ids = process_data(data)
    min_id = min(seat_ids)
    max_id = max(seat_ids)
    difference = set(range(min_id, max_id+1)).difference(seat_ids)
    return difference.pop()
