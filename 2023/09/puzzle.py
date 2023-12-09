# Advent Of Code 2023 - Puzzle 9
# https://adventofcode.com/2023/day/9
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-09 20:29:56.922426

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 9

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/9/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [int(number) for number in line.strip().split(" ")]
    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def extrapolate(sequence, backwards=False):
    sequence = list(sequence)
    factor = -1 if backwards else 1
    for level in range(len(sequence)):
        zero = True
        for i in range(len(sequence)-level-1):
            delta = sequence[i+1] - sequence[i]
            if delta != 0: zero = False
            sequence[i] = delta * factor
        if zero:
            break
        
    value = 0
    for i in range(level+1):
        delta = sequence[len(sequence)-level-1+i]
        value = delta + value * factor
    return value

def part_1(data):
    result = sum(map(extrapolate, data))
    print(f"part 1: {result}")
    
def part_2(data):
    result = sum((extrapolate(list(reversed(sequence)), True) for sequence in data))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)