def process_data(data):
    return map(int, data.splitlines())


def calc_fuel_req(masses):
    return list(filter(lambda x: x > 0, [mass // 3 - 2 for mass in masses]))


def solve_a(data):
    masses = process_data(data)
    fuel_req = calc_fuel_req(masses)
    return sum(fuel_req)


def solve_b(data):
    masses = process_data(data)
    fuel_req = calc_fuel_req(masses)
    total_fuel = sum(fuel_req)
    while sum(fuel_req) > 0:
        fuel_req = calc_fuel_req(fuel_req)
        total_fuel += sum(fuel_req)
    return total_fuel
