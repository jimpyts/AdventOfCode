import jimpy
import itertools
import collections


def increases(number):
    number = str(number)
    return all([(number[i] <= number[i + 1]) for i in range(len(number) - 1)])


def doubles(number):
    number = str(number)
    double_set = {str(i) * 2 for i in range(10)}
    for double in double_set:
        if double in number:
            return True
    return False


def doubles_alone(number):
    number = str(number)
    double_set = {str(i) * 2 for i in range(10)}
    for double in double_set:
        if double in number:
            return True
    return False


def filter_int_iterable(*rule_fns, iterable):
    for rule in rule_fns:
        iterable = [i for i in iterable if rule(i)]
    return iterable


def part_one(start, end):
    return filter(lambda x: increases(x) and doubles(x), range(start, end))


if __name__ == '__main__':
    data = jimpy.get_input("inputs/day4.txt", "-", data_type=int)
    start, end = data
    print(len(list(part_one(start, end))))
