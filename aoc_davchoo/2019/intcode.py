class IntCodeState:
    def __init__(self, memory):
        self.ip = 0

        self.memory = memory[::]

        self.output = []
        self.input = []
        self.iter_input = iter(self.input)

        self.current_opcode = 0
        self.parameters = []
        self.addressing_modes = []

        self.halt = False
        self.waiting_io = False
        self.wait_on_output = False

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


def read_parameters(num_parameters, state: IntCodeState):
    return (read(pos, mode, state) for pos, mode in zip(state.parameters[:num_parameters], state.addressing_modes))


def add(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]
    state.memory[dst] = src1 + src2


def mul(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]
    state.memory[dst] = src1 * src2


def read_input(state: IntCodeState):
    dst = state.parameters[0]
    try:
        state.memory[dst] = next(state.iter_input)
    except StopIteration:
        # Wait if we run out of input values
        state.ip -= 2  # Rerun input opcode
        state.waiting_io = True


def output_value(state: IntCodeState):
    value = next(read_parameters(1, state))
    state.output.append(value)
    if state.wait_on_output:
        state.waiting_io = True


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
        state.memory[dst] = 1
    else:
        state.memory[dst] = 0


def teq(state: IntCodeState):
    src1, src2 = read_parameters(2, state)
    dst = state.parameters[2]

    if src1 == src2:
        state.memory[dst] = 1
    else:
        state.memory[dst] = 0


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
        state.parameters = state.memory[state.ip:state.ip + num_parameters]
        state.ip += num_parameters

        opcode_func(state)
        if state.halt or state.waiting_io:
            break
