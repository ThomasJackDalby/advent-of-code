# Advent Of Code 2022 - Puzzle 22
# https://adventofcode.com/2022/day/22
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-02-08 07:18:51.671320
import sys

EMPTY = " "
FLOOR = "."
WALL = "#"

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    tiles = [line for line in lines[:-2]]
    max_width = max((len(line) for line in tiles))
    tiles = [line.ljust(max_width, " ") for line in tiles]
    map_widths = set((len(line) for line in tiles))
    if len(map_widths) != 1:
        raise Exception("Input file is corrupted, multiple widths detected.")

    commands = lines[-1]
    result = []
    number = ""
    for char in commands:
        if char == "L" or char == "R":
            result.append(int(number))
            result.append(char)
            number = ""
        else:
            number += char
    if number != "":
        result.append(int(number))
    return tiles, result

# 0, 1, 2, 3 => R, U, L, D

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

DELTAS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

def wrap_1d(value, min_value, max_value):
    if max_value <= min_value: raise Exception("Max value cannot be less than or equal to min value.")
    if value < min_value: return max_value - (min_value - value) + 1
    elif value > max_value: return min_value + (value - max_value) - 1
    else: return value

def wrap_2d(position, min_x, min_y, max_x, max_y):
    next_x = wrap_1d(position[0], min_x, max_x)
    next_y = wrap_1d(position[1], min_y, max_y)
    return (next_x, next_y) 

CUBE_FACES = [
    [-1,-1,]
]

# .00
# .0.
# 00.
# 0

# need to track which edges are connected, and what the transform between the facing direction is
#e.g. 0 -> 1 

def process(tiles, commands):
    map_height = len(tiles)
    map_width = len(tiles[0])
    # debug_map = [[tile for tile in line] for line in tiles]

    start_x = tiles[0].index(FLOOR)
    position = (start_x, 0)
    direction = 0
    # debug_map[position[1]][position[0]] = "X"

    def get_tile(position):
        return tiles[position[1]][position[0]]

    for command in commands:
        if command == "L": direction = (direction - 1) % 4
        elif command == "R": direction = (direction + 1) % 4
        else:
            for _ in range(command):
                delta = DELTAS[direction]
                next_tile = EMPTY
                next_position = position
                while next_tile == EMPTY:
                    next_position = add(next_position, delta)
                    next_position = wrap_2d(next_position, 0, 0, map_width-1, map_height-1)
                    next_tile = get_tile(next_position)
                
                if next_tile == FLOOR: position = next_position
                elif next_tile == WALL: break

    score = 1000 * (position[1]+1) + 4 * (position[0]+1) + direction
    print("score:", score)


if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    tiles, instructions = load_file(file_path)
    process(tiles, instructions)
