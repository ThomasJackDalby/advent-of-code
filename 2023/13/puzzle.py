# Advent Of Code 2023 - Puzzle 13
# https://adventofcode.com/2023/day/13
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-14 10:00:20.761391

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 13

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/13/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    with open(file_path, "r") as file: 
        lines = [line.strip() for line in file.readlines()]

    areas = []
    area = []
    for line in lines:
        if line != "": area.append(line)
        else:
            areas.append(area)
            area = []
    areas.append(area)
    return areas


def part_1(data):

    def find_reflection(lines):
        numbers = [int(line, 2) for line in lines]
        for x in range(len(numbers)-1):
            if numbers[x] == numbers[x+1]:
                if all(numbers[x-i] == numbers[x+i+1] for i in range(min(x+1, len(numbers)-x-1))):
                    return x+1
        return 0

    def find_reflections(region):
        row_result = 100 * find_reflection(["".join("0" if c == "." else "1" for c in line) for line in region])
        column_result = find_reflection(["".join("0" if c == "." else "1" for c in line) for line in ([region[j][i] for j in range(len(region))] for i in range(len(region[0])))])
        return row_result + column_result
    
    result = sum(find_reflections(region) for region in data)
    print(f"part 1: {result}")



def part_2(data):

    def are_mirrored(line_a, line_b, tolerance=1):
        number_of_equal = sum(1 for i in range(len(line_a)) if line_a[i] == line_b[i])
        return number_of_equal >= len(line_a) - tolerance#
        
    def find_smudged_reflection(lines, tolerance = 1):
        numbers = [int(line, 2) for line in lines]
        for x in range(len(numbers)-1):
            if are_mirrored(lines[x], lines[x+1], tolerance):
                to_check = min(x+1, len(lines)-x-1)
                number_of_valid = sum(1 for i in range(to_check) if numbers[x-i] == numbers[x+i+1])
                if number_of_valid == to_check - 1:
                    i = next(i for i in range(min(x+1, len(numbers)-x-1)) if numbers[x-i] != numbers[x+i+1])
                    number_of_errors = sum(1 for j in range(len(lines[0])) if lines[x-i][j] != lines[x+i+1][j])
                    if number_of_errors <= tolerance:
                        return x+1
        return 0

    def find_reflections(region, tolerance = 1):
        row_result = 100 * find_smudged_reflection(["".join("0" if c == "." else "1" for c in line) for line in region], tolerance)
        column_result = find_smudged_reflection(["".join("0" if c == "." else "1" for c in line) for line in ([region[j][i] for j in range(len(region))] for i in range(len(region[0])))], tolerance)
        return row_result + column_result
    
    result = sum(find_reflections(region, 1) for region in data)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)