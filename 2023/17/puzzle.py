# Advent Of Code 2023 - Puzzle 17
# https://adventofcode.com/2023/day/17
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-22 10:59:29.379553

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 17

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/17/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])
    
# --- Solution Start ----
from queue import PriorityQueue

def load_file(file_path):
    def parse_line(line):
        return [int(c) for c in line.strip()]
    
    with open(file_path, "r") as file:
       return [parse_line(line) for line in file.readlines()]

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

def part_1(data):

    width = len(data[0])
    height = len(data)
    
    distance_map = [None] * width * height
    distance_map[0] = 0

    def get_index(x, y):
        return y * width + x
    
    queue = [(0, 0)]
    while len(queue) > 0:
        x, y = queue.pop(0)
        distance = distance_map[get_index(x, y)]
        temperature = data[y][x]
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= width or ny < 0 or ny >= height: continue
            if distance_map[get_index(nx, ny)] is None or distance_map[get_index(nx, ny)] > distance:
                distance_map[get_index(nx, ny)] = distance + temperature
                queue.append((nx, ny))

    for y in range(height):
        print([distance_map[get_index(x, y)] for x in range(width)])

    result = None
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)