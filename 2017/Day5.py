
def get_input(filename="inputs/day5.txt"):
    with open(filename) as f:
        data = f.read()
        data = data.split("\n")
        return [int(i) for i in data if i]


def part_1():
    instructions = get_input()
    idx = 0
    steps = 0
    while 0 <= idx < len(instructions):
        instructions[idx] += 1
        idx += instructions[idx] - 1
        steps += 1
    return steps


def part_2():
    instructions = get_input()
    idx = 0
    steps = 0
    while 0 <= idx < len(instructions):
        increment = - 1 if (instructions[idx]) >= 3 else 1
        instructions[idx] += increment
        idx += instructions[idx] - increment
        steps += 1
    return steps


if __name__ == '__main__':
    print(part_1())
    print(part_2())
