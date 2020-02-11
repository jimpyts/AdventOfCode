import jimpy
import math
import itertools
import time


class Asteroid:
    def __init__(self, absolute):
        self.y, self.x = absolute
        self.absolute = self.x, self.y
        self.distance = None

    def __rshift__(self, other):
        return self.bearing(other)

    def __ge__(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)

    def __hash__(self):
        return hash(self.absolute)

    def __repr__(self):
        return f"Asteroid: ({self.x}, {self.y})"

    def bearing(self, other):
        theta = math.atan2(self.y - other.y, self.x - other.x) - math.pi / 2
        if theta < 0:
            theta += 2 * math.pi
        return math.degrees(theta)


def get_asteroids(data):
    asteroids = []

    for x, line in enumerate(data):
        for y, obj in enumerate(line):
            if obj == "#":
                asteroids.append(Asteroid((x, y)))

    return asteroids


def get_best_asteroid(asteroid_data):
    results = {asteroid: set() for asteroid in asteroid_data}

    for asteroid_1, asteroid_2 in itertools.permutations(asteroid_data, 2):
        bearing = asteroid_1 >> asteroid_2
        results[asteroid_1].add(bearing)

    asteroids_visible = 0
    best_asteroid = None

    for asteroid, unique_bearings in results.items():
        if len(unique_bearings) > asteroids_visible:
            asteroids_visible = len(unique_bearings)
            best_asteroid = asteroid

    return best_asteroid, asteroids_visible


def laser_asteroids(base, asteroid_data, limit):
    bearings = dict()
    products = [(base, asteroid) for asteroid in asteroid_data if base.absolute != asteroid.absolute]
    for base, other in products:
        bearing = base >> other
        other.distance = base >= other
        if bearing not in bearings:
            bearings[bearing] = [other]
        else:
            bearings[bearing].append(other)
            bearings[bearing].sort(key=lambda x: x.distance, reverse=True)

    counter = 0
    latest = None
    for bearing in itertools.cycle(sorted(bearings.keys())):
        if not bearings[bearing]:
            continue
        else:
            latest = bearings[bearing].pop()
            counter += 1
        if counter == limit:
            break

    return latest


def asteroids_to_grid(asteroids):
    grid = [["." for i in range(28)] for i in range(28)]
    for asteroid in asteroids:
        grid[asteroid.x][asteroid.y] = "#"
    return grid


def render_grid(grid):
    out = "\n".join(["".join(line) for line in grid])
    return out


def animate_laser(base, asteroid_data):
    grid = asteroids_to_grid(asteroid_data)
    bearings = dict()
    products = [(base, asteroid) for asteroid in asteroid_data if base.absolute != asteroid.absolute]
    for base, other in products:
        bearing = base >> other
        other.distance = base >= other
        if bearing not in bearings:
            bearings[bearing] = [other]
        else:
            bearings[bearing].append(other)
            bearings[bearing].sort(key=lambda x: x.distance, reverse=True)

    for bearing in itertools.cycle(sorted(bearings.keys())):
        if not bearings[bearing]:
            continue
        else:
            latest = bearings[bearing].pop()
            grid[latest.x][latest.y] = "."
            render_grid(grid)
            print(render_grid(grid), end="\r", flush=True)
            time.sleep(0.5)


def test():
    data = jimpy.get_input("inputs/day10.txt", "\n")
    asteroids = get_asteroids(data)
    base, part_one_result = get_best_asteroid(asteroids)
    animate_laser(base, asteroids)


if __name__ == '__main__':
    data = jimpy.get_input("inputs/day10.txt", "\n")
    asteroids = get_asteroids(data)
    base, part_one_result = get_best_asteroid(asteroids)
    print("Part one:", part_one_result)
    asteroid_200 = laser_asteroids(base, asteroids, 200)
    part_two_result = asteroid_200.x * 100 + asteroid_200.y
    print("Part two:", part_two_result)
