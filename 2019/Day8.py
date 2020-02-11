import jimpy


def slice_list(toslice, length):
    return [toslice[i:i + length] for i in range(0, len(toslice), length)]


def part_one(data):
    sliced_data = slice_list(data, 150)
    counter = 4000
    result = None
    for x in sliced_data:
        if x.count("0") < counter:
            result = x
            counter = x.count("0")
    return result.count("1") * result.count("2")


def part_two(data, white="*", black=" "):
    sliced_data = slice_list(data, 150)
    layered = list(zip(*sliced_data))
    result = []
    for pixel in layered:
        for i in pixel:
            if i in {"1", "0"}:
                if i == "1":
                    result.append(white)
                else:
                    result.append(black)
                break

    message = "".join(result)
    message = slice_list(message, 25)
    return "\n".join(message)


if __name__ == '__main__':
    data = jimpy.get_input("inputs/day8.txt")
    data = data.strip()

    print("Part one:", part_one(data))
    print("Part two:", part_two(data, white="X", black=" "), sep="\n")
