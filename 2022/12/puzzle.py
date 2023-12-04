# Advent Of Code 2022 - Puzzle 12
# https://adventofcode.com/2022/day/12
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-17 20:57:09.588946
import sys

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

class Grid:
    def __init__(self, width, height, data=None, default_value=None):
        self.width = width
        self.height = height
        self._data = data if data is not None else [[default_value for _ in range(width)] for _ in range(height)]

    def set(self, value, x, y=None):
        if y == None: x, y = x
        self._data[y][x] = value

    def get(self, x, y=None):
        if y == None: x, y = x
        return self._data[y][x]

    def get_all_xy(self):
        return ((x, y) for x in range(self.width) for y in range(self.height))

    def is_outside(self, x, y=None):
        if y == None: x, y = x
        return x >= self.width or x < 0 or y < 0 or y >= self.height

    def print(self):
        for y in range(self.height):
            line = "".join(str(self.get(x, y)).ljust(3) for x in range(self.width))
            print(line)

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    start = None
    end = None
    data = []
    for y, line in enumerate(lines):
        row_heights = []
        for x, char in enumerate(line):
            if char == "S":
                height = 0
                start = (x, y)
            elif char == "E":
                height = 25
                end = (x, y)
            else:
                height = ord(char) - ord("a")
            row_heights.append(height)
        data.append(row_heights)

    height_grid = Grid(len(data[0]), len(data), data)
    return height_grid, start, end

def create_distance_grid(height_grid, start):
    """Walks outwards from the start position, increasing the distance at each step such that every node knows it's distance from the start."""
    distance_grid = Grid(height_grid.width, height_grid.height)
    queue = [start]
    distance_grid.set(0, start[0], start[1])
    while(len(queue) > 0):
        current_position = queue.pop(0)
        next_distance = distance_grid.get(current_position) + 1
        for direction_delta in DIRECTIONS:
            next_position = add(current_position, direction_delta)
            if height_grid.is_outside(next_position): continue
            if height_grid.get(current_position) < height_grid.get(next_position) - 1: continue

            next_position_distance = distance_grid.get(next_position)
            if next_position_distance is None or next_position_distance > next_distance:
                queue.append(next_position)
                distance_grid.set(next_distance, next_position)
    return distance_grid

def search(height_grid, start, end):
    distance_grid = create_distance_grid(height_grid, start)

    # cant reach the end from the start
    min_distance = distance_grid.get(end)
    if min_distance is None: return None

    current = end # start at the end
    steps = 0
    while current != start:
        if current is None: # should never happen?
            return None
        changed_direction = False

        for direction_delta in DIRECTIONS:
            test_position = add(current, direction_delta) 
            if height_grid.is_outside(test_position): continue

            # can't travel to a space that is 2 higher than current position
            if height_grid.get(test_position) < height_grid.get(current) - 1: continue

            test_distance = distance_grid.get(test_position)
            if test_distance is None: continue # this step wasn't reached so skip it

            if min_distance is None or test_distance < min_distance:
                min_distance = test_distance
                min_position = test_position 
                changed_direction = True
        if not changed_direction:
            print("Failed to find a route")
            return None
        current = min_position
        steps += 1
    return steps

def optimise(height_grid, end):
    start_positions = [(x, y) for (x, y) in height_grid.get_all_xy() if height_grid.get(x, y) == 0]
    min_steps = None
    for start in start_positions:
        print(f"searching {start}")
        steps = search(height_grid, start, end)
        if steps is None:
            continue
        if min_steps is None or steps < min_steps:
            min_steps = steps
    return min_steps

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    height_grid, start, end = load_file(file_path)
    steps = optimise(height_grid, end)
    print(steps)
    