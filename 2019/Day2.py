import operator
import itertools
import jimpy


class IntcodeError(Exception):
    """Raised when intcode does not run according to expected rules"""
    pass


def get_input(filename="inputs/day2.txt"):
    with open(filename) as f:
        data = f.read()
        return [int(i) for i in data.split(",") if i]


def instruction_fn(opcode, intcode, *parameters):
    opcode_operators = {
        1: operator.add,
        2: operator.mul
    }
    assert opcode in opcode_operators
    val_1, val_2 = intcode[parameters[0]], intcode[parameters[1]]
    result = opcode_operators[opcode](val_1, val_2)
    return result


def run_program(intcode):
    pointer = 0
    opcode = intcode[0]
    while opcode != 99:
        try:
            address = intcode[pointer + 3]
            result = instruction_fn(opcode, intcode, *intcode[pointer + 1: pointer + 3])
            intcode[address] = result
        except (AssertionError, IndexError):
            raise IntcodeError
        pointer += 4
        opcode = intcode[pointer]
    return intcode[0]


def pre_process_intcode(intcode, noun=12, verb=2):
    intcode[1], intcode[2] = noun, verb
    return intcode


# @jimpy.time_it
def part_one(data):
    data = pre_process_intcode(data.copy())
    result = run_program(data)
    return result


def target_seek_program(data, target):
    for noun, verb in itertools.product(range(100), range(100)):
        intcode = data.copy()
        intcode = pre_process_intcode(intcode, noun=noun, verb=verb)
        if run_program(intcode) == target:
            return noun, verb


# @jimpy.time_it
def part_two(data, target=19690720):
    noun, verb = target_seek_program(data=data.copy(), target=target)
    return 100 * noun + verb


if __name__ == '__main__':
    intcode = jimpy.get_input("inputs/day2.txt", ",", data_type=int)
    print("Part one:", part_one(intcode))
    print("Part two:", part_two(intcode))
