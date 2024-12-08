# Advent Of Code 2024 - Puzzle 6
# https://adventofcode.com/2024/day/6
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-08 10:47:36.608897

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "test.txt"
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
    def parse_line(line):
        return line.strip()

    with open(file_path, "r") as file: 
        lines = file.readlines()

    start = None
    blocks = set()
    width = len(lines[0])
    height = len(lines)
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if tile == '#': blocks.add((x, y))
            elif tile == '^': start = (x, y)
    
    return start, blocks, width, height

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0)
]

def part_1(data):
    start, blocks, width, height = data
    print(start)
    print(blocks)
    visited = set([start])
    x, y = start
    direction = 2
    
    while True:
        dx, dy = DIRECTIONS[direction]
        nx = x + dx
        ny = y + dy
        print(nx, ny)
        if (nx, ny) in blocks:
            direction = (direction + 1) % 4
            continue
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            break
        x = nx
        y = ny
        visited.add((nx, ny))
    print(visited)
    result = len(visited)
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)