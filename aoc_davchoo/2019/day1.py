def process_data(data):
    return 0


def solve_a(data):
    masses = map(int, data.splitlines())
    fuel_req = [mass // 3 - 2 for mass in masses]
    return sum(fuel_req)


def solve_b(data):
    masses = map(int, data.splitlines())
    fuel_req = [mass // 3 - 2 for mass in masses]
    total_fuel = sum(fuel_req)
    while sum(fuel_req) > 0:
        fuel_req = list(filter(lambda x: x > 0, [mass // 3 - 2 for mass in fuel_req]))
        total_fuel += sum(fuel_req)
    return total_fuel
