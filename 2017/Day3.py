import math
from itertools import product


def part_1(i):
    if i == 1:
        return 0
    ring = math.ceil(i ** 0.5) // 2
    return abs((i - 1) % (ring * 2) - ring) + ring


class SpiralGen:
    dirs = {
        "E": (0, 1),
        "N": (-1, 0),
        "W": (0, -1),
        "S": (1, 0),
    }

    def __init__(self):
        self.grid = [[[] for i in range(50)] for j in range(50)]
        self.dir_idx = 0
        self.y = 25
        self.x = 25
        self.grid[self.y][self.x] = 1

    @property
    def grid_ref(self):
        return self.y, self.x

    @property
    def direction(self):
        idx = self.dir_idx % 4
        return list(self.dirs)[idx]

    @property
    def surrounding_value_sum(self):
        y_values = self.y-1, self.y, self.y+1
        x_values = self.x-1, self.x, self.x+1
        counter = 0
        for y, x in product(y_values, x_values):
            if self.grid[y][x]:
                counter += self.grid[y][x]
        return counter

    @property
    def left_val(self):
        idx = (self.dir_idx + 1) % 4
        left_dir = list(self.dirs)[idx]
        y = self.y + self.dirs[left_dir][0]
        x = self.x + self.dirs[left_dir][1]
        return self.grid[y][x]

    def move(self):
        self.y += self.dirs[self.direction][0]
        self.x += self.dirs[self.direction][1]
        if not self.left_val:
            self.dir_idx += 1

    def generate_spiral(self, limit):
        while self.grid[self.y][self.x] <= limit:
            self.move()
            self.grid[self.y][self.x] = self.surrounding_value_sum

    def part_2(self, limit):
        self.generate_spiral(limit)
        return self.grid[self.y][self.x]


x = SpiralGen()
print(part_1(361527))
print(x.part_2(361527))