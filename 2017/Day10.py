import jimpy
import collections
import functools


def rotate_list(to_rotate, rotate_by):
    data = collections.deque(to_rotate)
    data.rotate(rotate_by)
    return list(data)


def knot_hash(lengths, loop, skip_start=0, initial_rotate=0):
    loop = rotate_list(loop, -initial_rotate)
    rotation_count = 0
    curr_skip = skip_start
    for i in lengths:
        pinch = loop[:i]
        pinch = pinch[::-1]
        loop[:i] = pinch
        rotate_val = i + curr_skip
        rotation_count += rotate_val
        loop = rotate_list(loop, -rotate_val)
        curr_skip += 1
    loop = rotate_list(loop, rotation_count)
    loop = rotate_list(loop, initial_rotate)
    return loop, curr_skip, rotation_count


@jimpy.time_it
def part_one(data):
    result, _, _ = knot_hash(data, loop=list(range(256)))
    return result[0] * result[1]


def str_to_bytes(string):
    return [ord(i) for i in string if i]


def get_input_knot_hash(filename="inputs/day10.txt"):
    with open(filename) as f:
        data = f.read().strip()
        print(data)
        return str_to_bytes(data) + [17, 31, 73, 47, 23]


def condense_hash(sparse_hash):
    assert len(sparse_hash) == 256
    out = []
    for i in range(16):
        decs = sparse_hash[i * 16:i * 16 + 16]
        xored = functools.reduce(lambda a, b: a ^ b, decs)
        out.append(xored)
    return out


# @jimpy.time_it
def part_two():
    lengths = get_input_knot_hash()
    stored_skip = 0
    initial_rotate = 0
    loop = list(range(256))
    for i in range(64):
        loop, stored_skip, initial_rotate = knot_hash(lengths, skip_start=stored_skip, loop=loop, initial_rotate=initial_rotate)
        # if i == 1:
        #     assert loop[1] == 154
        print(i, loop)
    dense_hash = condense_hash(loop)
    hex_vals = [hex(i)[2:] for i in dense_hash]
    hex_vals = ["0" + i if len(i) == 1 else i for i in hex_vals]
    return "".join(hex_vals)


if __name__ == '__main__':
    data = jimpy.get_input("inputs/day10.txt", ",", data_type=int)
    # print("Part one:", part_one(data))
    print("Part two:", part_two())


if __name__ == '__main__':
    def reverse_sublist(lst, start, end):
        sublist = []
        for i in range(start, end + 1):
            sublist.append(lst[i % len(lst)])
        reverse = list(reversed(sublist))
        j = 0
        for i in range(start, end + 1):
            lst[i % len(lst)] = reverse[j]
            j += 1
        return lst


    inp = '120,93,0,90,5,80,129,74,1,165,204,255,254,2,50,113'
    lengths = []
    for c in inp:
        lengths.append(ord(c))
    for i in [17, 31, 73, 47, 23]:
        lengths.append(i)
    numbers = [x for x in range(0, 256)]
    curr_pos = 0
    skip_size = 0

    for _ in range(64):
        for l in lengths:
            numbers = reverse_sublist(numbers, curr_pos, curr_pos + l - 1)
            curr_pos += (l + skip_size)
            skip_size += 1
        print(_, numbers)

    dense_list = []
    for i in range(16):
        for j in range(16):
            if j == 0:
                acc = numbers[(i * 16) + j]
            else:
                acc = acc ^ numbers[(i * 16) + j]
        dense_list.append(acc)

    final = ""
    for x in dense_list:
        h = hex(x)[2:]
        if len(h) == 1:
            h = "0" + h
        final += h
    print("Expected:", final)
