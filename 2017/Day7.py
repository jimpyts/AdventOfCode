import re


def get_input(filename="inputs/day7.txt"):
    with open(filename) as f:
        data = f.read()
        return [i for i in data.split("\n") if i]


def breakdown_program(program_str):
    name, weight, _, dependants = re.search('([a-z]+) \((\d+)\)( -> )?(.*)', program_str).groups()
    dependants = set(dependants.split(", ")) if _ else set()
    return name, int(weight), dependants


class Program:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children


def part1():
    data = get_input()
    names = set()
    all_set = set()
    for program_str in data:
        name, _, child_set = breakdown_program(program_str)
        names.add(name)
        all_set = all_set | child_set
    return names ^ all_set


def explore_tree(root_program_name):
    data = [Program(*breakdown_program(i)) for i in get_input()]
    stack = dict([(program.name, program) for program in data])


def part2():
    data = [Program(*breakdown_program(i)) for i in get_input()]
    stack = dict([(program.name, program) for program in data])
    root = stack[list(part1())[0]]
    main_towers = dict([(dependant, 0) for dependant in root.children])
    pass

part2()