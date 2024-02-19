# Advent Of Code 2023 - Puzzle 21
# https://adventofcode.com/2023/day/21
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-30 21:16:49.381834

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 21

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/21/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [c for c in line.strip()]

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def find_start(data):
    for x, line in enumerate(data):
        for y, tile in enumerate(line):
            if tile == "S":
                return (x, y)
    raise Exception()

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

def part_1(data):
    width = len(data[0])
    height = len(data)

    sx, sy = find_start(data)
    data[sy][sx] = "."

    next_queue = set()
    queue = [(sx, sy)]

    for step in range(26501365):
        for nx, ny in queue:
            for d in range(4):
                dx, dy = DIRECTIONS[d]
                x = nx + dx
                y = ny + dy

                # if x < 0 or x >= width or y < 0 or y >= height:
                #     continue
                
                if data[y % height][x % width] == ".":
                    next_queue.add((x, y))
           
        queue = next_queue
        next_queue = set()         

    result = len(queue)
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)