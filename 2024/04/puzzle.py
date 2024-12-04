# Advent Of Code 2024 - Puzzle 4
# https://adventofcode.com/2024/day/4
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-04 08:10:17.313874

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 4

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/4/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip()

    with open(file_path, "r") as file: 
        return [parse_line(line) for line in file.readlines()]

def part_1(data):
    result = 0
    x_max = len(data[0])
    y_max = len(data)

    def check(x_min, x_max, y_min, y_max, dx, dy):
        count = sum((1 
                    for x in range(x_min, x_max)
                    for y in range(y_min, y_max)
                    if (data[y][x] == "X" and
                        data[y+dy][x+dx] == "M" and
                        data[y+2*dy][x+2*dx] == "A" and
                        data[y+3*dy][x+3*dx] == "S")))
        print(f"{count} for ({dx},{dy})")
        return count

    result += check(0, x_max-3, 0, y_max, 1, 0)
    result += check(3, x_max, 0, y_max, -1, 0)
    result += check(0, x_max, 0, y_max-3, 0, 1)
    result += check(0, x_max, 3, y_max, 0, -1)

    result += check(0, x_max-3, 0, y_max-3, 1, 1)
    result += check(3, x_max, 3, y_max, -1, -1)
    result += check(3, x_max, 0, y_max-3, -1, 1)
    result += check(0, x_max-3, 3, y_max, 1, -1)
    print(f"part 1: {result}")
    
def part_2(data):
    x_max = len(data[0])
    y_max = len(data)
    result = 0
    for x in range(0, x_max-2):
        for y in range(0, y_max-2):
            if data[y+1][x+1] != "A": continue
            if not ((data[y][x] == "M" and data[y+2][x+2] == "S") or
                    (data[y][x] == "S" and data[y+2][x+2] == "M")): continue
            if not ((data[y+2][x] == "M" and data[y][x+2] == "S") or
                    (data[y+2][x] == "S" and data[y][x+2] == "M")): continue
            result += 1
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)