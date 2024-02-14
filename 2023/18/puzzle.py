# Advent Of Code 2023 - Puzzle 18
# https://adventofcode.com/2023/day/18
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-23 13:31:49.202202

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 18

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/18/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----
def parse_direction(direction_key):
    if direction_key == "R": return 0
    if direction_key == "U": return 1
    if direction_key == "L": return 2
    if direction_key == "D": return 3

def load_file(file_path):
    def parse_line(line):
        direction_key, amount, colour = line.strip().split(" ")
        return parse_direction(direction_key), int(amount), colour
    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]

DIRECTIONS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

def get_outside_path(data, switch=False):
    path = set()
    x, y = 0, 0
    for direction, small_amount, large_amount in data:
        amount = small_amount if not switch else large_amount
        dx, dy = DIRECTIONS[direction]
        for _ in range(amount):
            x += dx
            y += dy
            if dy != 0: path.add((x, y))
        if dy == 0: path.add((x, y))
    return path

def sum_path(path):
    min_y = min((y for _, y in path))
    max_y = max((y for _, y in path))
    height = max_y - min_y + 1

    total = 0
    for y in range(height):
        nodes = list(sorted(nx for nx, ny in path if ny == y))
        include_section = False
        section_start = None      
        row_total = len(nodes)
        previous_linked_above = None
        for i, x in enumerate(nodes):
            linked_above = (x, y-1) in path
            linked_below = (x, y+1) in path
            if include_section:
                row_total += x - section_start - 1
            if linked_above and linked_below: 
                include_section = not include_section # crossed a single dig line
            else:
                if i == 1: include_section = False
                if previous_linked_above is None:
                    previous_linked_above = linked_above
                else:
                    if (previous_linked_above and linked_below) or (not previous_linked_above and linked_above):
                        include_section = not include_section
                    row_total += x - section_start - 1
                    previous_linked_above = None
            section_start = x # section start can only be previous x
        total += row_total
    return total

def part_1(data):
    path = get_outside_path(data)
    result = sum_path(path)
    print(f"part 1: {result}")

def part_2(data):
    path = get_outside_path(data)
    result = sum_path(path)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    # part_2(data)