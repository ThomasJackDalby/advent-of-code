# Advent Of Code 2024 - Puzzle 1
# https://adventofcode.com/2024/day/1
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-01 07:35:55.055940

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 1

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/1/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return int(line[0:5]), int(line[8:13])

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    data = zip(*(sorted(x) for x in zip(*data)))
    result = sum(abs(a - b) for a, b in data)
    print(f"part 1: {result}")
    
def part_2(data):
    left = list(sorted(entry[0] for entry in data))
    right = list(sorted(entry[1] for entry in data))

    result = 0
    for a in left:
        result += a * sum(1 for b in right if a == b)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)