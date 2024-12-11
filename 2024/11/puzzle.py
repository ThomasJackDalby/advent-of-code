# Advent Of Code 2024 - Puzzle 11
# https://adventofcode.com/2024/day/11
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-11 10:21:20.355836

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 11

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/11/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [int(x) for x in line.strip().split(" ")]
    with open(file_path, "r") as file: 
        return parse_line(file.readline())

CACHE = { }

def transform(value):
    if value == 0: return [1]

    # split the stone in two
    str_value = str(value)
    if len(str_value) % 2 == 0:
        mid = len(str_value) // 2
        x = int(str_value[:mid])
        y = int(str_value[mid:])
        return [x, y]
    
    # otherwise mult by 2024
    return [value * 2024]

def solve(value, steps):
    if steps == 0: 
        return 1
    
    if (value, steps) in CACHE:
        return CACHE[(value, steps)]
    
    total = 0
    for sub_value in transform(value):
        total += solve(sub_value, steps - 1)
    CACHE[(value, steps)] = total
    return total

def part_1(data):
    result = sum(solve(x, 25) for x in data)
    print(f"part 1: {result}")
    
def part_2(data):
    result = sum(solve(x, 75) for x in data)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)