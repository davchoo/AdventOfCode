def process_data(data):
    code = []
    for line in data.splitlines():
        operation, argument = line.split(" ")
        argument = int(argument)
        code.append((operation, argument))
    return code


def run_code(code):
    instructions_ran = set()
    ip = 0
    acc = 0
    while True:
        if ip in instructions_ran:
            return "infinite", acc
        elif ip >= len(code):
            return "terminated", acc
        instructions_ran.add(ip)

        operation, argument = code[ip]
        if operation == "acc":
            acc += argument
        elif operation == "jmp":
            ip += argument - 1
        ip += 1


def solve_a(data):
    code = process_data(data)
    result, acc = run_code(code)
    assert result == "infinite"
    return acc


def solve_b(data):
    code = process_data(data)
    for line, instruction in enumerate(code):
        operation, argument = instruction
        if operation == "acc":
            continue
        elif operation == "nop":
            operation = "jmp"
        elif operation == "jmp":
            operation = "nop"

        fixed_code = code.copy()
        fixed_code[line] = (operation, argument)

        result, acc = run_code(fixed_code)
        if result == "terminated":
            return acc
