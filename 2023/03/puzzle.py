# Advent Of Code 2023 - Puzzle 3
# https://adventofcode.com/2023/day/3
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-03 06:34:40.006939

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 3

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/3/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip()
    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def extract_details(data):
    for y, line in enumerate(data):
        x = 0
        while x < len(line):
            if line[x].isnumeric():
                sx = x
                while x < len(line) and line[x].isnumeric():
                    x += 1
                x -= 1
                ex = x
                yield (sx, y, line[sx:ex+1])
            elif line[x] != ".":
                yield (x, y, line[x])
            x += 1

def part_1(data):
    MAX_X = len(data[0])
    MAX_Y = len(data)

    details = list(extract_details(data))
    numbers = [(x, y, detail) for x, y, detail in details if detail[0].isnumeric()]
    parts = { (x, y) : detail for x, y, detail in details if not detail[0].isnumeric() } 

    def check_if_part_number(x, y, number):
        min_x = max(x-1, 0)
        max_x = min(x+len(number), MAX_X-1)
        min_y = max(y-1, 0)
        max_y = min(y+1, MAX_Y-1)

        for py in range(min_y, max_y+1):
            for px in range(min_x, max_x+1):
                if (px, py) in parts:
                    return True
        return False

    part_numbers = [(x, y, number) for x, y, number in numbers if check_if_part_number(x, y, number)]

    total = sum(int(part_number) for x, y, part_number in part_numbers) 
    print(f"part 1: {total}")

def part_2(data):
    MAX_X = len(data[0])
    MAX_Y = len(data)

    details = list(extract_details(data))
    numbers = [(x, y, detail) for x, y, detail in details if detail[0].isnumeric()]
    parts = { (x, y) : detail for x, y, detail in details if not detail[0].isnumeric() } 
    gears = { (x, y) : [] for x, y in parts if parts[(x, y)] == "*" }

    def find_gear(x, y, number):
        min_x = max(x-1, 0)
        max_x = min(x+len(number), MAX_X-1)
        min_y = max(y-1, 0)
        max_y = min(y+1, MAX_Y-1)
        for py in range(min_y, max_y+1):
            for px in range(min_x, max_x+1):
                if (px, py) in gears:
                    return gears[(px, py)]
        return None
                    
    for x, y, number in numbers:
        gear = find_gear(x, y, number)
        if gear is None:
            continue
        gear.append(int(number))

    total = 0
    for x, y in gears:
        gear_numbers = gears[(x, y)]
        if len(gear_numbers) != 2:
            continue
        gear_ratio = gear_numbers[0] * gear_numbers[1]
        total += gear_ratio

    print(f"part 2: {total}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)