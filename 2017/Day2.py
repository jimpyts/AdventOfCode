from time import time
from functools import wraps
import jimpy


def time_it(func):
    @wraps(func)
    def time_it_wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} took {end-start} seconds")
        return res
    return time_it_wrapper


def get_input(filename="inputs/day2.txt"):
    with open(filename) as f:
        data = f.read()
        data = list(data.split("\n"))
        data = [line.split("\t") for line in data if line]
        data = [[int(x) for x in line] for line in data]
        return data


def row_diff(row):
    return max(row) - min(row)


def row_div(row):
    for divisor in row:
        for dividend in row:
            res, rem = divmod(dividend, divisor)
            if rem == 0 and res != 1:
                return res


@time_it
def part1():
    data = get_input()
    data = jimpy.get_input("inputs/day2.txt", "\n", "\t", data_type=int)
    return sum([row_diff(row) for row in data])


@time_it
def part2():
    data = jimpy.get_input("inputs/day2.txt", "\n", "\t", data_type=int)
    return sum([row_div(row) for row in data])


if __name__ == '__main__':
    print(part1())
    print(part2())
