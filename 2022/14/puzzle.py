# Advent Of Code 2022 - Puzzle 14
# https://adventofcode.com/2022/day/14
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-19 11:11:14.855806
import sys

ORIGIN_X = 500
ORIGIN_Y = 0

EMPTY = 0
WALL = 1
SAND = 2
SPAWN = 3

def sign(a):
    if a == 0: return 0
    elif a < 0: return -1
    else: return 1 

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def subtract(a, b):
    return (a[0] - b[0], a[1] - b[1])

class Grid:
    def __init__(self, width, height, min_x, min_y):
        self.width = width
        self.height = height
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = self.min_x + width
        self.max_y = self.min_y + height
        self.min = (min_x, min_y)
        self._data = [[EMPTY for _ in range(width)] for _ in range(height)]

        tx, ty = self._get_local_xy((self.max_x, self.max_y))
        print(f"{tx=} {ty=}")
        print(f"{self.width=} {self.height=}")
        print(f"{self.min_x=} {self.max_x=}")
        print(f"{self.min_y=} {self.max_y=}")

    def _get_local_xy(self, xy):
        return subtract(xy, self.min)

    def get(self, x, y = None):
        xy = (x, y) if isinstance(x, int) else x
        tx, ty = self._get_local_xy(xy)
        if tx < 0 or tx >= self.width: raise Exception(f"{tx=} {x=} is out of range")
        if ty < 0 or ty >= self.height: raise Exception(f"{tx=} {x=} is out of range")
        return self._data[ty][tx]

    def set(self, value, x, y = None):
        xy = (x, y) if isinstance(x, int) else x
        tx, ty = self._get_local_xy(xy)
        if tx < 0 or tx >= self.width: raise Exception(f"{tx=} {x=} is out of range")
        if ty < 0 or ty >= self.height: raise Exception(f"{tx=} {x=} is out of range")
        self._data[ty][tx] = value

    def print(self):
        chars = [".", "#", "o", "+"]

        numbers = [str(i).rjust(3) for i in range(self.min_x, self.max_x)]

        for i in range(0, 3):
            print(" " + "".join(num[i] for num in numbers) + " ")
        print("X"+"-"*self.width+"X")
        row = 0
        for line in self._data:
            text_line = "|"+"".join(chars[c] for c in line) + f"| {row}"
            row += 1
            print(text_line)
        print("X"+"-"*self.width+"X")

def load_file(file_path, add_floor=True):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    lines = [[(int(x), int(y)) for x, y in (p.split(",") for p in line.split(" -> "))] for line in lines]
    x_values = [point[0] for line in lines for point in line] + [ORIGIN_X]
    y_values = [point[1] for line in lines for point in line] + [ORIGIN_Y]
    
    max_x, max_y = max(x_values) + 1, max(y_values) + 1
    if add_floor:
        min_y = 0
        max_y += 2
        height = max_y
        min_x = 500 - height
        max_x = 500 + height + 1
        width = max_x - min_x
    else:
        min_x, min_y = min(x_values), min(y_values)
        width, height = max_x - min_x, max_y - min_y

    grid = Grid(width, height, min_x, min_y)
    grid.set(SPAWN, 500, 0)
    
    for line in lines:
        sx, sy = line[0]
        for tx, ty in line[1:]:
            dx = int(sign(tx - sx))
            dy = int(sign(ty - sy))
            grid.set(WALL, sx, sy)
            while sx != tx or sy != ty:
                grid.set(WALL, sx, sy)
                sx, sy = sx + dx, sy + dy
            grid.set(WALL, sx, sy)

    if add_floor:
        for x in range(min_x, max_x):
            grid.set(WALL, x, max_y-1)
    return grid

def simulate(grid):
    # sand falls until it can't fall down, down left or right.

    sand_flowing_forever = False
    number_of_grains = 0
    while not sand_flowing_forever:
        if grid.get(ORIGIN_X, ORIGIN_Y) == SAND:
            break

        sand = (ORIGIN_X, ORIGIN_Y)
        while True:
            sand_x, sand_y = sand
            if sand_x <= grid.min_x or sand_x >= grid.max_x-1 or sand_y >= grid.max_y-1:
                sand_flowing_forever = True
                break

            if grid.get(sand_x, sand_y + 1) == 0:
                sand = add(sand, (0, 1))
            elif grid.get(sand_x - 1, sand_y + 1) == 0:
                sand = add(sand, (-1, 1))
            elif grid.get(sand_x + 1, sand_y + 1) == 0:
                sand = add(sand, (1, 1))
            else:
                number_of_grains += 1
                break
        
        grid.set(SAND, sand)
    grid.print()
    print("Finished")
    print(f"{number_of_grains=}")

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    grid = load_file(file_path, False)
    grid.print()

    simulate(grid)



