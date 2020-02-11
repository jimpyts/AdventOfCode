import jimpy


def get_root(data):
    orbited, orbiters = zip(*data)
    return list(set(orbited) - set(orbiters))[0]


def create_orbit_dict(data):
    orbited, orbiters = zip(*data)

    orbit_dict = {o: set() for o in orbited}
    for a, b in data:
        orbit_dict[a].add(b)
    return orbit_dict


@jimpy.time_it
def part_one(orbit_dict, root):
    counter = 0
    depth = 0
    to_crawl = [root, ]
    while to_crawl:
        depth += 1
        new_to_crawl = []
        for i in to_crawl:
            if i in orbit_dict:
                new_to_crawl += list(orbit_dict[i])
        to_crawl = new_to_crawl
        counter += len(to_crawl) * depth
    return counter


def path_to_code(orbit_dict, destination):
    path = []
    while "COM" not in path:
        for orbited, orbiters in orbit_dict.items():
            if destination in orbiters:
                path.append(orbited)
                destination = orbited
                break
    return path


@jimpy.time_it
def part_two(orbit_dict):
    youpath = path_to_code(orbit_dict, "YOU")
    sanpath = path_to_code(orbit_dict, "SAN")
    for idx, val in enumerate(youpath):
        if val in sanpath:
            return idx + sanpath.index(val)


if __name__ == '__main__':
    data = jimpy.get_input("inputs/day6.txt", "\n", ")")
    orbit_dict = create_orbit_dict(data)
    root = get_root(data)
    print("Part one:", part_one(orbit_dict, root))
    print("Part two:", part_two(orbit_dict))
