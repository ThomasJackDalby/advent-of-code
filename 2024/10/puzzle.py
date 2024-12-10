# Advent Of Code 2024 - Puzzle 10
# https://adventofcode.com/2024/day/10
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-10 07:53:36.080092

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 10

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/10/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [int(x) if x != "." else -1 for x in line.strip()]

    with open(file_path, "r") as file: 
        lines = [parse_line(line) for line in file.readlines()]
    width = len(lines[0])
    height = len(lines)
    return width, height, lines

DELTAS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

def search_all(data, start):
    max_x, max_y, heights = data
    sx, sy = start
    def search(x, y):
        current_height = heights[y][x]
        if current_height == 9: return 1

        total = 0
        for dx, dy in DELTAS:
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= max_x or ny < 0 or ny >= max_y: continue
            if heights[ny][nx] != current_height+1: continue

            total += search(nx, ny)
        return total
    return search(sx, sy)


def search_unique(data, start):
    max_x, max_y, heights = data
    queue = [start]
    reachable = set()
    while len(queue) > 0:
        x, y = queue.pop(0)
        current_height = heights[y][x]
        if current_height == 9:
            reachable.add((x, y))

        for dx, dy in DELTAS:
            nx = x + dx
            ny = y + dy

            if nx < 0 or nx >= max_x or ny < 0 or ny >= max_y: continue
            if heights[ny][nx] != current_height+1: continue
            queue.append((nx, ny))
    
    return len(reachable) 

def get_trail_heads(data):
    _, _, heights = data
    for y, row in enumerate(heights):
        for x, tile in enumerate(row):
            if tile == 0:
                yield (x, y)

def part_1(data):
    result = 0
    for node in get_trail_heads(data):
        result += search_unique(data, node)
    print(f"part 1: {result}")
    
def part_2(data):
    result = 0
    for node in get_trail_heads(data):
        result += search_all(data, node)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":

    data = get_data()
    part_1(data)
    part_2(data)