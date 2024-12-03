# Advent Of Code 2024 - Puzzle 3
# https://adventofcode.com/2024/day/3
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-03 07:22:24.112735

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 3

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/3/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

import re

def load_file(file_path):
    def parse_line(line):
        return line.strip()
    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    p = re.compile("mul\(([0-9]*),([0-9]*)\)")
    result = 0
    for line in data:
        for match in p.finditer(line):
            result += int(match.group(1)) * int(match.group(2))
    print(f"part 1: {result}")
    
def part_2(data):
    p = re.compile("mul\(([0-9]*),([0-9]*)\)|do\(\)|don't\(\)")
    result = 0
    enabled = True
    for line in data:
        for match in p.finditer(line):
            if match.group(0) == "do()": enabled = True
            elif match.group(0) == "don't()": enabled = False
            elif enabled:
                result += int(match.group(1)) * int(match.group(2))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)