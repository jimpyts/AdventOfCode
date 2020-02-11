from collections import Counter


def get_input(filename="inputs/day4.txt"):
    with open(filename) as f:
        data = f.read()
        data = data.split("\n")
        return [i for i in data if i]


def part_1():
    data = get_input()
    for passphrase in data:
        passphrase = passphrase.split()
        yield(int(len(passphrase) == len(set(passphrase))))


def part_2():
    data = get_input()
    for passphrase in data:
        passphrase = passphrase.split()
        yield(int(len(passphrase) == len(set(passphrase)) and
                  len(set(map(HashableCounter, passphrase))) == len(passphrase)))


class HashableCounter(Counter):
    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


if __name__ == '__main__':
    print(sum(part_1()))
    print(sum(part_2()))
