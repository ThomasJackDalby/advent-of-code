# Advent Of Code 2020 - Puzzle 1
# https://adventofcode.com/2020/day/1
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-11-24 06:54:45.276801

import os
import sys

INPUT_FILE_NAME = "input.txt"

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]

    return lines

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        print(os.path.abspath("../.."))
        sys.path.append(os.path.abspath("../.."))
        from setup import cache_input_file
        cache_input_file(2023, 1)
    file_path = INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1]
    return load_file(file_path)

# --- Solution Start ----

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()