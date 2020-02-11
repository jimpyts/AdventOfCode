def get_input(filename="inputs/day9.txt"):
    with open(filename) as f:
        data = f.read()
    return data.strip()


def part_one(data=get_input()):
    total = 0
    level = 0
    garbage = False
    ignore = False

    for i in data:
        if ignore:
            ignore = not ignore
            continue
        elif i is "!":
            ignore = not ignore
        elif i is "<":
            garbage = True
        elif i is ">":
            garbage = False
        elif i is "{" and not garbage:
            level += 1
        elif i is "}" and not garbage:
            total += level
            level -= 1
        else:
            continue
    return total


def part_two(data=get_input()):
    garbage_count = 0
    garbage = False
    ignore = False
    for i in data:
        if ignore:
            ignore = not ignore
            continue
        elif i is "!":
            ignore = True
        elif i is "<" and not garbage:
            garbage = True
        elif i is ">":
            garbage = False
        elif i is "{" and not garbage:
            continue
        elif i is "}" and not garbage:
            continue
        else:
            if garbage:
                garbage_count += 1
            else:
                continue
    return garbage_count


if __name__ == '__main__':
    print("Part one:", part_one())
    print("Part two:", part_two())
