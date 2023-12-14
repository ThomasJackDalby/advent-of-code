# Advent Of Code {year} - Puzzle {day}
# https://adventofcode.com/{year}/day/{day}
# Tom Dalby - https://github.com/thomasjackdalby
# Date: {datetime}

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = {year}
DAY = {day}

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies={{"session": session_id}})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip().split(" ")

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    result = None
    print(f"part 1: {{result}}")
    
def part_2(data):
    result = None
    print(f"part 2: {{result}}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)