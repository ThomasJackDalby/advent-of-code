# Advent Of Code 2024 - Puzzle 2
# https://adventofcode.com/2024/day/2
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-02 07:49:08.465037

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 2

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/2/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [int(x) for x in line.strip().split(" ")]

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def check_report(report):
    # checks whether the report:
    # 1. is either all increasing or decreasing
    # 2. increase/decreases by a delta between 1 and 3 (or -1 and -3)
    # if these rules fail, returns the problem index or -1 if the report is safe.

    if report[0] == report[-1]:
        return len(report)-1
    
    # need a factor to adjust the allowed delta if we're decreasing
    factor = -1 if report[0] > report[-1] else 1

    for i, level in enumerate(report[1:]):
        previous_level = report[i]
        delta = (level - previous_level) * factor
        if delta < 1 or delta > 3:
            return i + 1
    return -1

def check_report_2(report):
    result = check_report(report)
    if result == -1:
        return True
    if check_report(report[:result] + report[result+1:]) == -1:
        return True
    if check_report(report[:result-1] + report[result:]) == -1:
        return True
    return False

def part_1(data):
    result = sum(1 for report in data if check_report(report) == -1)
    print(f"part 1: {result}")
    
def part_2(data):
    result = sum(1 for report in data if check_report_2(report))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)