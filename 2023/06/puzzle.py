# Advent Of Code 2023 - Puzzle 6
# https://adventofcode.com/2023/day/6
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-07 21:06:15.451121

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 6

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/6/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        while "  " in line:
            line = line.replace("  ", " ")
        return [int(number.strip()) for number in line.split(":")[1].strip().split(" ")]
    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]

def part_1(data):
    times, distances = data
    result = 1
    for i in range(len(times)):
        time = times[i]
        distance = distances[i]
        min_charge = next(c for c in range(0, time) if (time - c) * c > distance)
        max_charge = next(c for c in range(time, 0, -1) if (time - c) * c > distance)
        result *= max_charge - min_charge + 1

    print(f"part 1: {result}")
    
def part_2(data):
    times, distances = data
    time = int("".join(str(t) for t in times))
    distance = int("".join(str(d) for d in distances))

    min_charge = next(c for c in range(0, time) if (time - c) * c > distance)
    max_charge = next(c for c in range(time, 0, -1) if (time - c) * c > distance)
    result = max_charge - min_charge + 1
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)