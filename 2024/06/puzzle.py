# Advent Of Code 2024 - Puzzle 6
# https://adventofcode.com/2024/day/6
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-08 10:47:36.608897

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 6

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/6/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    with open(file_path, "r") as file: 
        lines = file.readlines()

    start = None
    blocks = set()
    width = len(lines[0])-1
    height = len(lines)
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == '#': blocks.add((x, y))
            elif tile == '^': start = (x, y)
    
    if start is None:
        raise Exception("Not found start")
    return start, blocks, width, height

DIRECTIONS = [
    (0, 1), # DOWN
    (-1, 0), # LEFT
    (0, -1), # UP
    (1, 0) # RIGHT
]

DOWN_MASK = 0b0010
LEFT_MASK = 0b0100
UP_MASK = 0b0001
RIGHT_MASK = 0b1000

MASKS = [
    DOWN_MASK,
    LEFT_MASK,
    UP_MASK,
    RIGHT_MASK
]

def print_map(width, height, blocks, blockers, visited):
    # print the map for debug purposes.
    for y in range(height):
        line = ""
        for x in range(width):
            if (x, y) in blocks: line += "#"
            elif (x, y) in blockers: line += "O"
            else:
                dir = visited.get((x, y), 0)
                vert = (dir & (UP_MASK | DOWN_MASK)) > 0
                hor = (dir & (LEFT_MASK | RIGHT_MASK)) > 0
                if hor and not vert: line += "-"
                elif vert and not hor: line += "|"
                elif vert and hor: line += "+"
                else: line += "."
        print(line)

def part_1(data):
    start, blocks, width, height = data
    visited = set([start])
    x, y = start
    direction = 2
    
    while True:
        dx, dy = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy
        if (nx, ny) in blocks:
            direction = (direction + 1) % 4
            continue
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            break
        x = nx
        y = ny
        visited.add((nx, ny))

    result = len(visited)
    print(f"part 1: {result}")

def part_2(data):
    start, blocks, width, height = data

    def solve(x, y, direction, visited, check_loop = False):
        # delta = DIRECTIONS[]
        # obstacle = x + 
        obstacles = set()
        while True:
            dx, dy = DIRECTIONS[direction]
            nx = x + dx
            ny = y + dy

            # turn right if the position ahead is blocked
            # if (nx, ny) in blocks or (check_loop and (nx, ny == )):
            #     direction = (direction + 1) % 4
            #     continue

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                if check_loop:
                    return False # if we go outside the map, we haven't looped
                else:
                    return obstacles
                
            if check_loop:
                previous_direction = visited.get((x, y), 0)
                mask = MASKS[direction]
                if (mask & previous_direction) > 0:
                    return True
            else:
                # need to clone visited otherwise we effect future loops
                if solve(x, y, (direction + 1) % 4, dict(visited), True):
                    obstacles.add((nx, ny))
            
            # update the visited map with the direction we were facing
            visited[(nx, ny)] = visited.get((nx, ny), 0) | MASKS[direction]
            
            # move to next position
            x = nx
            y = ny
            
    obstacles = solve(*start, 2, {}, False)
    result = len(obstacles)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)