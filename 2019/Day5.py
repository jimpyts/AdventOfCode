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

    def __init__(self, intcode, input_value):
        self.intcode_stored = intcode.copy()
        self.pointer = 0
        self.intcode = intcode.copy()
        self.input_value = input_value
        self.test_outputs = []

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
        self.pointer = 0
        instruction = self[self.pointer]
        opcode, *parameter_modes = self.parse_opcode_instruction(instruction)
        while opcode != 99:
            assert opcode in self.opcode_fns
            parameters_len = self.opcode_parameter_lengths[opcode]
            parameters = [self.pointer + i + 1 for i in range(parameters_len)]
            parameters = list(zip(parameters, parameter_modes))
            self.opcode_fns[opcode](*parameters)
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
        self[p1_val] = self.input_value
        self.pointer += 2

    def output(self, p1):
        p1_val, p1_mode = p1
        p1_val = self[p1_val]
        p1_val = p1_val if p1_mode == 1 else self[p1_val]
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


def test(intcode, isfile, input_val, attr_to_test, attr_args, expected_result, *methods_to_call):
    test_data = jimpy.get_input(intcode, ",", data_type=int) if isfile else [int(i) for i in intcode.split(",") if i]
    test_comp = IntcodeComputer(test_data, input_val)
    try:
        for method, *args in methods_to_call:
            getattr(test_comp, method)(*args)
        result = getattr(test_comp, attr_to_test)
        if type(result) == types.MethodType:
            if attr_args:
                result = getattr(test_comp, attr_to_test)(*attr_args)
            else:
                result = getattr(test_comp, attr_to_test)()
        assert result == expected_result
        print("Success")
    except:
        raise IntcodeError("Failed")


def run_tests():
    test("inputs\day2.txt", True, None, "result", None, 2842648, ("pre_run", 12, 2), ("run",))
    test("inputs\day2.txt", True, None, "target_seek", [19690720], (90, 74))
    test("1002,4,3,4,33", False, None, "intcode", None, [1002, 4, 3, 4, 99], ("run",))
    test("3,0,4,0,99", False, 123456, "test_outputs", None, [123456], ("run", ))
    test("3,9,8,9,10,9,4,9,99,-1,8", False, 9, "test_outputs", None, [0], ("run", ))
    test("3,9,7,9,10,9,4,9,99,-1,8", False, 5, "test_outputs", None, [1], ("run", ))
    test("3,3,1108,-1,8,3,4,3,99", False, 8, "test_outputs", None, [1], ("run", ))
    test("3,3,1107,-1,8,3,4,3,99", False, 8, "test_outputs", None, [0], ("run", ))
    test("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", False, 0, "test_outputs", None, [0], ("run", ))
    test("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", False, 5, "test_outputs", None, [1], ("run", ))
    test("3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99",
         False, 8, "test_outputs", None, [1000], ("run", ))



if __name__ == '__main__':
    # run_tests()

    data = jimpy.get_input("inputs\day5.txt", ",", data_type=int)
    comp = IntcodeComputer(data, 1)
    comp.run()
    print("Day one:", comp.test_outputs[-1])
    comp = IntcodeComputer(data, 5)
    comp.run()
    print("Day two:", comp.test_outputs[-1])

