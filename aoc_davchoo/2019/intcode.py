import collections
from copy import copy, deepcopy


class IntCodeMachine:
    def __init__(self, memory, user_input=None):
        self.ip = 0

        self.memory = collections.defaultdict(int)
        self.memory.update(enumerate(memory))

        self.output = []
        self.input = None
        self.iter_input = None
        if user_input is None:
            user_input = []
        self.set_input(user_input)

        self.current_opcode = 0
        self.parameters = []
        self.addressing_modes = []
        self.relative_base = 0

        self.halt = False
        self.return_output = False
        self.waiting_input = False

        # opcode: (function, number of parameters)
        self.opcode_map = {
            1: (IntCodeMachine.add, 3),
            2: (IntCodeMachine.mul, 3),
            3: (IntCodeMachine.read_input, 1),
            4: (IntCodeMachine.output_value, 1),
            5: (IntCodeMachine.jit, 2),
            6: (IntCodeMachine.jif, 2),
            7: (IntCodeMachine.tlt, 3),
            8: (IntCodeMachine.teq, 3),
            9: (IntCodeMachine.adj_rel_base, 1),
            99: (IntCodeMachine.halt_machine, 0)
        }

    def set_input(self, user_input):
        if isinstance(user_input, int):
            user_input = [user_input]
        self.input = user_input
        self.iter_input = iter(user_input)
        self.waiting_input = False

    def read(self, position, addressing_mode):
        if addressing_mode == 0:
            # Position Mode
            return self.memory[position]
        elif addressing_mode == 1:
            # Immediate Mode
            return position
        elif addressing_mode == 2:
            # Relative Mode
            return self.memory[position + self.relative_base]

    def write(self, position, value, addressing_mode):
        if addressing_mode == 0:
            # Position Mode
            self.memory[position] = value
        elif addressing_mode == 2:
            # Relative Mode
            self.memory[position + self.relative_base] = value

    def read_parameters(self, num_parameters):
        return (self.read(pos, mode) for pos, mode in zip(self.parameters[:num_parameters], self.addressing_modes))

    def add(self):
        src1, src2 = self.read_parameters(2)
        dst = self.parameters[2]
        self.write(dst, src1 + src2, self.addressing_modes[2])

    def mul(self):
        src1, src2 = self.read_parameters(2)
        dst = self.parameters[2]
        self.write(dst, src1 * src2, self.addressing_modes[2])

    def read_input(self):
        dst = self.parameters[0]
        try:
            self.write(dst, next(self.iter_input), self.addressing_modes[0])
        except StopIteration:
            # Wait if we run out of input values
            self.ip -= 2  # Rerun input opcode
            self.waiting_input = True

    def output_value(self):
        value = next(self.read_parameters(1))
        self.output.append(value)

    def jit(self):
        value, jmp_target = self.read_parameters(2)
        if value != 0:
            self.ip = jmp_target

    def jif(self):
        value, jmp_target = self.read_parameters(2)
        if value == 0:
            self.ip = jmp_target

    def tlt(self):
        src1, src2 = self.read_parameters(2)
        dst = self.parameters[2]

        if src1 < src2:
            self.write(dst, 1, self.addressing_modes[2])
        else:
            self.write(dst, 0, self.addressing_modes[2])

    def teq(self):
        src1, src2 = self.read_parameters(2)
        dst = self.parameters[2]

        if src1 == src2:
            self.write(dst, 1, self.addressing_modes[2])
        else:
            self.write(dst, 0, self.addressing_modes[2])

    def adj_rel_base(self):
        val, = self.read_parameters(1)
        self.relative_base += val

    def halt_machine(self):
        self.halt = True

    def run(self):
        while True:
            if self.halt or self.waiting_input:
                return None
            opcode = self.memory[self.ip]
            self.current_opcode = opcode % 100
            self.addressing_modes = opcode // 100
            self.addressing_modes = [int(digit) for digit in str(self.addressing_modes).zfill(4)][::-1]

            self.ip += 1

            opcode_func, num_parameters = self.opcode_map[self.current_opcode]
            self.parameters = [self.memory[self.ip + offset] for offset in range(num_parameters)]
            self.ip += num_parameters

            opcode_func(self)

            if self.return_output and opcode_func == IntCodeMachine.output_value:
                return self.output[-1]

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}

        new_machine = copy(self)
        new_machine.memory = deepcopy(self.memory, memo=memodict)
        new_machine.input = deepcopy(self.input, memo=memodict)
        new_machine.iter_input = deepcopy(self.iter_input, memo=memodict)
        new_machine.output = deepcopy(self.output, memo=memodict)

        return new_machine


def load_program(text):
    program = list(map(int, text.split(",")))
    return program


def run_program(memory, user_input=None):
    machine = IntCodeMachine(memory, user_input)
    machine.run()

    return machine.memory, machine.output
