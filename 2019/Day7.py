import jimpy
import itertools
import types


class IntcodeError(Exception):
    pass


class IntcodeComputer:
    opcode_parameter_lengths = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
    }

    def __init__(self, intcode, phase_setting, input_values):
        self.intcode_stored = intcode.copy()
        self.pointer = 0
        self.intcode = intcode.copy()
        self.phase_setting = phase_setting
        self.phase_setting_used = False
        self.input_values = input_values
        self.input_value_pointer = 0
        self.test_outputs = []

    def __repr__(self):
        return f"INTCODE COMPUTER {self.phase_setting}"

    def __getitem__(self, item):
        return self.intcode[item]

    def __setitem__(self, key, value):
        self.intcode[key] = value

    def pre_run(self, noun, verb):
        self[1] = noun
        self[2] = verb

    @staticmethod
    def parse_opcode_instruction(opcode_instruction):
        assert opcode_instruction >= 0
        opcode_instruction = str(opcode_instruction)
        opcode_instruction = "0" * (5 - len(opcode_instruction)) + opcode_instruction
        p3_mode, p2_mode, p1_mode, *opcode = opcode_instruction
        opcode = int("".join(opcode))
        return opcode, int(p1_mode), int(p2_mode), int(p3_mode)

    def run(self):
        # self.pointer = 0
        instruction = self[self.pointer]
        opcode, *parameter_modes = self.parse_opcode_instruction(instruction)
        while opcode != 99:
            assert opcode in self.opcode_fns
            parameters_len = self.opcode_parameter_lengths[opcode]
            parameters = [self.pointer + i + 1 for i in range(parameters_len)]
            parameters = list(zip(parameters, parameter_modes))
            self.opcode_fns[opcode](*parameters)
            if opcode == 4:
                return self.test_outputs[-1]
            instruction = self[self.pointer]
            opcode, *parameter_modes = self.parse_opcode_instruction(instruction)

    def result(self):
        return self.intcode[0]

    def add(self, p1, p2, p3):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        p3_val, p3_mode = p3
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_3 = self[p3_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        self[val_3] = val_1 + val_2
        self.pointer += 4

    def mul(self, p1, p2, p3):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        p3_val, p3_mode = p3
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_3 = self[p3_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        self[val_3] = val_1 * val_2
        self.pointer += 4

    def input(self, p1):
        p1_val, p1_mode = p1
        p1_val = self[p1_val]
        if self.phase_setting_used:
            self[p1_val] = self.input_values[self.input_value_pointer]
            self.input_value_pointer += 1
            self.input_value_pointer = min(self.input_value_pointer, len(self.input_values))
        else:
            self[p1_val] = self.phase_setting
            self.phase_setting_used = True
        # self[p1_val] = int(input("TEST: "))
        self.pointer += 2

    def output(self, p1):
        p1_val, p1_mode = p1
        p1_val = self[p1_val]
        p1_val = p1_val if p1_mode == 1 else self[p1_val]
        # print(p1_val)
        self.test_outputs.append(p1_val)
        self.pointer += 2

    def jump_if_true(self, p1, p2):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        if val_1:
            self.pointer = val_2
        else:
            self.pointer += 3

    def jump_if_false(self, p1, p2):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        if not val_1:
            self.pointer = val_2
        else:
            self.pointer += 3

    def less_than(self, p1, p2, p3):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        p3_val, p3_mode = p3
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_3 = self[p3_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        self[val_3] = int(val_1 < val_2)
        self.pointer += 4

    def equals(self, p1, p2, p3):
        p1_val, p1_mode = p1
        p2_val, p2_mode = p2
        p3_val, p3_mode = p3
        val_1 = self[p1_val]
        val_2 = self[p2_val]
        val_3 = self[p3_val]
        val_1 = val_1 if p1_mode == 1 else self[val_1]
        val_2 = val_2 if p2_mode == 1 else self[val_2]
        self[val_3] = int(val_1 == val_2)
        self.pointer += 4

    @property
    def opcode_fns(self):
        return {
            1: self.add,
            2: self.mul,
            3: self.input,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
        }

    def target_seek(self, target):
        for noun, verb in itertools.product(range(100), range(100)):
            self.intcode = self.intcode_stored.copy()
            self.pre_run(noun, verb)
            self.run()
            if self.result() == target:
                return noun, verb

    @staticmethod
    def amplify(data, phases):
        previous_output = 0
        for phase in phases:
            comp = IntcodeComputer(data, phase, [previous_output])
            comp.run()
            previous_output = comp.test_outputs[0]
        return previous_output

    @staticmethod
    def amplify_loop(data, phases):
        comps = [IntcodeComputer(data, phase, []) for phase in phases]
        previous_output = 0
        counter = 0
        while True:
            comp = comps[counter]
            comp.input_values.append(previous_output)
            result = comp.run()
            counter += 1
            counter %= 5
            if not result:
                break
            previous_output = result
        return previous_output


def part_one(data):
    cmax = 0
    for p in itertools.permutations(range(5), 5):
        result = IntcodeComputer.amplify(data, p)
        if result > cmax:
            cmax = result
    return cmax


def part_two(data):
    cmax = 0
    for phase_permutation in itertools.permutations(range(9, 4, -1), 5):
        result = IntcodeComputer.amplify_loop(data, phase_permutation)
        if result > cmax:
            cmax = result
    return cmax


if __name__ == '__main__':
    data = jimpy.get_input("inputs\day7.txt", ",", data_type=int)
    print("Part one:", part_one(data))
    print("Part one:", part_two(data))
