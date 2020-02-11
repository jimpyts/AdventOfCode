import jimpy
import itertools


class Planet:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.xv = 0
        self.yv = 0
        self.zv = 0

    def __or__(self, other):
        for attr in ('x', 'y', 'z'):
            self_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if self_val > other_val:
                setattr(self, attr + "v", getattr(self, attr + "v") - 1)
                setattr(other, attr + "v", getattr(other, attr + "v") + 1)
            elif other_val > self_val:
                setattr(self, attr + "v", getattr(self, attr + "v") + 1)
                setattr(other, attr + "v", getattr(other, attr + "v") - 1)

    def move(self):
        self.x += self.xv
        self.y += self.yv
        self.z += self.zv

    def pot(self):
        return sum(map(abs, (self.x, self.y, self.z)))

    def kin(self):
        return sum(map(abs, (self.xv, self.yv, self.zv)))

    def energy(self):
        return self.kin() * self.pot()

    def __repr__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel=<x={self.xv}, y={self.yv}, z={self.zv}>"

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.xv, self.yv, self.zv))


data = jimpy.get_input("inputs/day12.txt", "\n")
data = [i[1:-1] for i in data if i]
data = [eval(f"Planet({i})") for i in data if i]

# data = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>"""
# data = [i[1:-1] for i in data.split("\n") if i]
# data = [eval(f"Planet({i})") for i in data if i]


# data="""<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>"""
# data = [i[1:-1] for i in data.split("\n") if i]
# data = [eval(f"Planet({i})") for i in data if i]



seen_before = set()

while tuple(map(hash, data)) not in seen_before:
# while True:
    seen_before.add(tuple(map(hash, data)))
    for a, b in itertools.combinations(data, 2):
        a | b
    for planet in data:
        planet.move()

print(len(seen_before))


# for i in range(1000):
#     for a, b in itertools.combinations(data, 2):
#         a | b
#     for planet in data:
#         planet.move()
#
#
# for i in data:
#     print(i)
#
# print(sum([i.energy() for i in data]))
#
