# Advent Of Code 2023 - Puzzle 3
# https://adventofcode.com/2023/day/3
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-03 06:34:40.006939

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 3

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/3/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip()
    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    MAX_X = len(data[0])
    MAX_Y = len(data)
    print(f"{MAX_X=} {MAX_Y=}")

    def check_if_part(sx, ex, y):
        min_x = max(sx-1, 0)
        max_x = min(ex+1, MAX_X-1)
        min_y = max(y-1, 0)
        max_y = min(y+1, MAX_Y-1)

        for j in range(min_y, max_y+1):
            line = data[j]
            for i in range(min_x, max_x+1):
                char = line[i]
                if char == ".": continue
                if char.isnumeric(): continue
                return True
        return False

    def get_numbers():
        for y, line in enumerate(data):
            x = 0
            # print(line)
            while x < len(line):
                if line[x].isnumeric():
                    sx = x
                    while x < len(line) and line[x].isnumeric():
                        x += 1
                    ex = x-1
                    yield (sx, ex, y)
                x += 1

    # for sx, ex, y in get_numbers():
    #     result = check_if_part(sx, ex, y)
    #     print("------------------")
    #     print(f"{sx=} {ex=} {y=} {int(data[y][sx:ex+1])}")
    #     for dy in [-1, 0, 1]:
    #         print(data[y+dy][sx-1:ex+2])
    #     print(result)

    total = sum(int(data[y][sx:ex+1]) for sx, ex, y in get_numbers() if check_if_part(sx, ex, y))
    print(total)

def part_2(data):
    pass

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)