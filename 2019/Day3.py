import jimpy
import re


def parse_inst(x):
    out = re.match("([A-Z]{1})(\d+)", x).groups()
    dir, dist = out[0], int(out[1])
    return dir, dist


def wire_path_generator(instructions):
    curr_X = 0
    curr_Y = 0
    for inst in instructions:
        dir, dist = parse_inst(inst)
        for _ in range(dist):
            if dir == "R":
                curr_X += 1
            elif dir == "D":
                curr_Y -= 1
            elif dir == "L":
                curr_X -= 1
            elif dir == "U":
                curr_Y += 1
            yield curr_X, curr_Y


def steps_to_coord(instructions, coord_dict):
    steps = 0
    for curr_coord in wire_path_generator(instructions):
        steps += 1
        if curr_coord in coord_dict:
            coord_dict[curr_coord] = steps
    return coord_dict


def get_intersections(wires):
    wire_1, wire_2 = wires
    w1coords = set(wire_path_generator(wire_1))
    w2coords = set(wire_path_generator(wire_2))
    return w2coords & w1coords


@jimpy.time_it
def part_one(wires):
    return min([(abs(a) + abs(b)) for a, b in get_intersections(wires)])


@jimpy.time_it
def part_two(wires):
    intersections = get_intersections(wires)
    w1dict = {intersection: 0 for intersection in intersections}
    w2dict = w1dict.copy()
    w1dict = steps_to_coord(wires[0], w1dict)
    w2dict = steps_to_coord(wires[1], w2dict)
    return min([(w1dict[key] + w2dict[key]) for key in w1dict.keys()])


if __name__ == '__main__':
    wires = jimpy.get_input("inputs/day3.txt", "\n", ",")
    print("Part one:", part_one(wires))
    print("Part two:", part_two(wires))
