# Advent Of Code 2023 - Puzzle 14
# https://adventofcode.com/2023/day/14
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-14 19:51:19.613277

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 14

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/14/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip()

    with open(file_path, "r") as file: 
        lines = [parse_line(line) for line in file.readlines()]

    height = len(lines)
    width = len(lines[0])
    static_rocks = set()
    ball_rocks = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "O": ball_rocks.add((x, y))
            elif char == "#": static_rocks.add((x, y))
    return width, height, static_rocks, ball_rocks

def display(width, height, static_rocks, ball_rocks):
    lines = [["."] * width for i in range(height)]
    for x, y in static_rocks: lines[y][x] = "#"
    for x, y in ball_rocks: lines[y][x] = "O"
    for line in lines: print("".join(line)) 
    print()

DIRECTIONS = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0),
]

SORT_DIRECTIONS = [
    lambda rock: rock[1],
    lambda rock: rock[0],
    lambda rock: -rock[1],
    lambda rock: -rock[0],
]

def tilt(data, direction):
    width, height, static_rocks, ball_rocks = data
    dx, dy = DIRECTIONS[direction]
    for (x, y) in sorted(ball_rocks, key=SORT_DIRECTIONS[direction]):
        ball_rocks.remove((x, y))
        nx, ny = x+dx, y+dy
        while nx >= 0 and ny >= 0 and nx < width and ny < height and (nx, ny) not in ball_rocks and (nx, ny) not in static_rocks:
            x, y = nx, ny
            nx, ny = x+dx, y+dy
        ball_rocks.add((x, y))

def part_1(data):
    _, height, _, ball_rocks = data

    tilt(data, 0)

    result = sum(height - y for _, y in ball_rocks)
    print(f"part 1: {result}")
    
def part_2(data):
    _, height, _, ball_rocks = data

    hashed = {}
    total_number_of_cycles = 1000000000
    index = 0
    while index < total_number_of_cycles:
        for direction in range(4):
            tilt(data, direction)
        index += 1
        
        hash_value = hash(tuple(ball_rocks))
        if hash_value in hashed:
            previous_index = hashed[hash_value]
            delta = index - previous_index
            while index + delta < total_number_of_cycles:
                index += delta
        hashed[hash_value] = index

    result = sum(height - y for _, y in ball_rocks)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)