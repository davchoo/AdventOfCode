import collections


class IntCodeState:
    def __init__(self, memory):
        self.ip = 0

        self.memory = collections.defaultdict(int)
        self.memory.update(enumerate(memory))

        self.output = []
        self.input = []
        self.iter_input = iter(self.input)

        self.current_opcode = 0
        self.parameters = []
        self.addressing_modes = []
        self.relative_base = 0

        self.halt = False
        self.waiting_io = False
        self.wait_on_output = False
        self.io_direction = ""

    def set_input(self, user_input):
        self.input = user_input
        self.iter_input = iter(user_input)
        self.waiting_io = False


def read(position, addressing_mode, state: IntCodeState):
    if addressing_mode == 0:
        # Position Mode
        return state.memory[position]
    elif addressing_mode == 1:
        # Immediate Mode
        return position
    elif addressing_mode == 2:
        # Relative Mode
        return state.memory[position + state.relative_base]


def write(position, value, addressing_mode, state: IntCodeState):
    if addressing_mode == 0:
        # Position Mode
        state.memory[position] = value
    elif addressing_mode == 2:
        # Relative Mode
        state.memory[position + state.relative_base] = value


def read_parameters(num_parameters, state: IntCodeState):
    return (read(pos, mode, state) for pos, mode in zip(state.parameters[:num_parameters], state.addressing_modes))


def add(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]
    write(dst, src1 + src2, state.addressing_modes[2], state)


def mul(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]
    write(dst, src1 * src2, state.addressing_modes[2], state)


def read_input(state: IntCodeState):
    dst = state.parameters[0]
    try:
        write(dst, next(state.iter_input), state.addressing_modes[0], state)
    except StopIteration:
        # Wait if we run out of input values
        state.ip -= 2  # Rerun input opcode
        state.waiting_io = True
        state.io_direction = "Read"


def output_value(state: IntCodeState):
    value = next(read_parameters(1, state))
    state.output.append(value)
    if state.wait_on_output:
        state.waiting_io = True
        state.io_direction = "Write"


def jit(state: IntCodeState):
    value, jmp_target = read_parameters(2, state)
    if value != 0:
        state.ip = jmp_target


def jif(state: IntCodeState):
    value, jmp_target = read_parameters(2, state)
    if value == 0:
        state.ip = jmp_target


def tlt(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]

    if src1 < src2:
        write(dst, 1, state.addressing_modes[2], state)
    else:
        write(dst, 0, state.addressing_modes[2], state)


def teq(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]

    if src1 == src2:
        write(dst, 1, state.addressing_modes[2], state)
    else:
        write(dst, 0, state.addressing_modes[2], state)


def adj_rel_base(state: IntCodeState):
    val, = read_parameters(1, state)
    state.relative_base += val


def halt(state: IntCodeState):
    state.halt = True


opcode_map = {
    1: (add, 3),
    2: (mul, 3),
    3: (read_input, 1),
    4: (output_value, 1),
    5: (jit, 2),
    6: (jif, 2),
    7: (tlt, 3),
    8: (teq, 3),
    9: (adj_rel_base, 1),
    99: (halt, 0)
}


def load_program(text):
    program = list(map(int, text.split(",")))
    return program


def run_program(memory, user_input=None):
    if user_input is None:
        user_input = []

    state = IntCodeState(memory)
    state.set_input(user_input)

    run_with_state(state)

    return state.memory, state.output


def run_with_state(state: IntCodeState):
    while True:
        opcode = state.memory[state.ip]
        state.current_opcode = opcode % 100
        state.addressing_modes = opcode // 100
        state.addressing_modes = [int(digit) for digit in str(state.addressing_modes).zfill(4)][::-1]

        state.ip += 1

        opcode_func, num_parameters = opcode_map[state.current_opcode]
        state.parameters = [state.memory[state.ip + offset] for offset in range(num_parameters)]
        state.ip += num_parameters

        opcode_func(state)
        if state.halt or state.waiting_io:
            break
