# Advent Of Code 2024 - Puzzle 7
# https://adventofcode.com/2024/day/7
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-08 08:30:15.136513

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 7

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/7/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        target, values = line.strip().split(":")
        target = int(target)
        values = [int(v) for v in values.strip().split(" ")]
        return target, values

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def solve(target, current, operators, values, part_2=False):
    if len(values) == 0:
        if target == current: return operators
        return None

    result = solve(target, current + values[0], operators + ["+"], values[1:], part_2)
    if result is not None: return result

    result = solve(target, current * values[0], operators + ["*"], values[1:], part_2)
    if result is not None: return result

    if part_2:
        result = solve(target, int(str(current) + str(values[0])), operators + ["||"], values[1:], part_2)
        if result is not None: return result
    return None

def part_1(data):

    result = 0
    for target, values in data:
        x = solve(target, values[0], [], values[1:])
        if x is not None:
            result += target
    print(f"part 1: {result}")
    
def part_2(data):
    result = 0
    for target, values in data:
        x = solve(target, values[0], [], values[1:], True)
        if x is not None:
            result += target
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)