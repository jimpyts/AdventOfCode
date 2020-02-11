with open("inputs/day6.txt") as f:
    data = f.read()
    data = [int(i) for i in data.split() if i]


class Memory:
    def __init__(self, initial_data):
        self.data = initial_data
        self.sets = {tuple(self.data)}

    def __len__(self):
        return len(self.sets)

    def redistribute(self):
        idx = self.data.index(max(self.data))
        val = self.data[idx]
        self.data[idx] = 0
        for i in range(val):
            idx += 1
            idx = idx % len(self.data)
            self.data[idx] += 1

    def run(self):
        start = len(self)
        while start == 1 or len(self) != start:
            start = len(self)
            self.redistribute()
            self.sets.add(tuple(self.data))

    def run(self):
        start = len(self)
        while start == 1 or len(self) != start:
            start = len(self)
            self.redistribute()
            self.sets.add(tuple(self.data))


if __name__ == '__main__':
    x = Memory(data)
    x.run()
    print("Part 1:", len(x))

    y = Memory(x.data)
    y.run()
    print("Part 2:", len(y))
