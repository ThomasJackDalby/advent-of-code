# Advent Of Code 2024 - Puzzle 15
# https://adventofcode.com/2024/day/15
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2025-01-15 08:47:11.499568

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 15

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/15/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

LEFT = "<"
RIGHT = ">"
UP = "^"
DOWN = "v"

DIRECTIONS = {
    LEFT : 0,
    UP : 1,
    RIGHT : 2,
    DOWN : 3,
}
DELTAS = [
    (-1, 0),
    (0, -1),
    (1, 0),
    (0, 1),
]

WALL = "#"
BOX = "O"
ROBOT = "@"
EMPTY = "."

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        split_index = lines.index("")
        tiles = [[tile for tile in line] for line in lines[:split_index]]
        commands = "".join(lines[split_index:])
    return tiles, commands

def find_robot_position(tiles):
    for ry, line in enumerate(tiles):
        for rx, tile in enumerate(line): 
            if tile == ROBOT:
                return rx, ry

def get_gps_score(tiles):
    score = 0
    for y, line in enumerate(tiles):
        for x, tile in enumerate(line): 
            if tiles[y][x] == BOX:
                score += 100 * y + x
    return score

def get_direction_delta(direction):
    direction_index = DIRECTIONS[direction]
    return DELTAS[direction_index]

def part_1(data):
    tiles, directions = data
    print(tiles)
    print(directions)

    # find robot start position
    rx, ry = find_robot_position(tiles)

    def move_robot_to_tile(tx, ty): 
        # note, this does not check if tile move is allowed   
        nonlocal rx, ry
        tiles[ry][rx] = EMPTY
        rx = tx
        ry = ty
        tiles[ry][rx] = ROBOT

    for direction in directions:
        dx, dy = get_direction_delta(direction)

        def try_to_push_boxes(tx, ty):
            # can try to push the boxes if there is empty space behind the last box
            x = tx
            y = ty
            while tiles[y][x] == BOX:
                x += dx
                y += dy
            if tiles[y][x] == EMPTY:
                tiles[y][x] = BOX
                move_robot_to_tile(tx, ty)

        # check the position it wants to move to
        tx = rx + dx
        ty = ry + dy
        tile = tiles[ty][tx]
        if tile == EMPTY: move_robot_to_tile(tx, ty)
        elif tile == BOX: try_to_push_boxes(tx, ty)
        
    for line in tiles:
        print("".join(line))

    result = get_gps_score(tiles)
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)