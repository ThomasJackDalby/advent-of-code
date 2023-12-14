# Advent Of Code 2023 - Puzzle 11
# https://adventofcode.com/2023/day/11
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-11 13:00:57.405387

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 11

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/11/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    with open(file_path, "r") as file: 
        return [(x, y) for y, line in enumerate(file.readlines()) for x, c in enumerate(line.strip()) if c == "#"]

def part_1(data):
    width = max((x for (x, _) in data))+1
    height = max((y for (_, y) in data))+1  
    
    column_count = [0]*width
    row_count = [0]*height
    for x, y in data:
        column_count[x] += 1
        row_count[y] += 1

    column_offset = [0]*width
    offset = 0
    for i in range(width):
        column_offset[i] = offset
        if column_count[i] == 0:
            offset += 1

    row_offset = [0]*height
    offset = 0
    for i in range(height):
        row_offset[i] = offset
        if row_count[i] == 0:
            offset += 1

    #print(f"{column_offset=}")
    #print(f"{row_offset=}")

    factor = 1000000-1

    result = 0
    for i in range(len(data)):
        sx, sy = data[i]
        for j in range(i+1, len(data)):
            ex, ey = data[j]
            distance = abs(ex-sx) + abs(ey-sy) 
            x_offset = abs(column_offset[ex] - column_offset[sx]) * factor
            y_offset = abs(row_offset[ey] - row_offset[sy]) * factor
            altered_distance = distance + x_offset + y_offset
            #prin#t(f"{i=} {j=} {sx=} {sy=} {ex=} {ey=} {distance=} {altered_distance=}")
            result += altered_distance
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)