# Advent Of Code 2023 - Puzzle 12
# https://adventofcode.com/2023/day/12
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-14 06:06:22.975960

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 12

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/12/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        pattern, groups = line.strip().split(" ")
        return pattern, list(map(int, groups.split(",")))

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    

    def evaluate(pattern, groups):
        print(f"{pattern}|{groups}")
        if len(groups) == 0 and "#" not in pattern: return 1
        group = groups[0]
        total = 0
        for i in range(len(pattern)-group+1):
            if all(pattern[i + j] in ("#", "?") for j in range(group)) and (len(pattern) <= i + group or pattern[i + group] in (".", "?")):
                next_pattern = pattern[i+group+1:] if i+group < len(pattern) else "" 
                next_groups = groups[1:] if len(groups) > 1 else []
                total += evaluate(next_pattern, next_groups)
        return total

    for pattern, groups in data[-1:]:
        total = evaluate(pattern, groups)
        print(f"{pattern} {groups} {total}")

    # result = sum(evaluate(pattern, groups) for pattern, groups in data)
    # print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)