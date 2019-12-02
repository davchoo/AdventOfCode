from more_itertools import take


def add(ip, memory):
    # Add Source address, Source Address, Destination Address
    src1, src2, dst = take(3, ip)
    memory[dst] = memory[src1] + memory[src2]


def mul(ip, memory):
    # Multiply Source address, Source Address, Destination
    src1, src2, dst = take(3, ip)
    memory[dst] = memory[src1] * memory[src2]


opcode_map = {
    1: add,
    2: mul,
    99: lambda x, y: None  # Halt
}


def run_program(memory):
    ip = iter(memory)
    current_opcode = next(ip)
    while True:
        opcode_map[current_opcode](ip, memory)
        if current_opcode == 99:
            # Halt
            break
        current_opcode = next(ip)

    return memory[0], memory
