# Advent Of Code 2023 - Puzzle 2
# https://adventofcode.com/2023/day/2
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-02 19:33:14.856663

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 2

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/2/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

COLOURS = [
    "green",
    "red",
    "blue"
]

def load_file(file_path):
    def parse_line(line):
        game_info, set_info = line.strip().split(":")
        results = []
        for set in set_info.strip().split(";"):
            result = [0]*3
            for colour_group in set.split(","):
                amount, colour = colour_group.strip().split(" ")
                if len(colour) == 3: result[0] = int(amount)
                elif len(colour) == 5: result[1] = int(amount)
                elif len(colour) == 4: result[2] = int(amount)
                else: raise Exception()
            results.append(result)
        return results  

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

# --- Solution Start ----

def part_1(data):
    MAX_RED = 12
    MAX_GREEN = 13
    MAX_BLUE = 14

    result = 0
    for i, game in enumerate(data):
        red = max((s[0] for s in game))
        green = max((s[1] for s in game))
        blue = max((s[2] for s in game))
        if red <= MAX_RED and green <= MAX_GREEN and blue <= MAX_BLUE:
            result += i + 1
    print("part 1", result)

def part_2(data):
    result = 0
    for game in data:
        red = max((s[0] for s in game))
        green = max((s[1] for s in game))
        blue = max((s[2] for s in game))
        result += red * green * blue
    print("part 2", result)

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)
