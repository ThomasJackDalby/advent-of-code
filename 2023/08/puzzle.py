# Advent Of Code 2023 - Puzzle 8
# https://adventofcode.com/2023/day/8
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-08 16:00:08.182085

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 8

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/8/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    directions = [0 if d == "L" else 1 for d in lines[0]]

    def parse_line(line):
        node, links = [part.strip() for part in line.split("=")]
        return node, (links[1:4],links[6:9])
    
    return directions, { node : links for node, links in (parse_line(line) for line in lines[2:])}

def part_1(data):
    directions, nodes = data
    current = "AAA"
    index = 0
    while current != "ZZZ":
        direction = directions[index % len(directions)]
        current = nodes[current][direction]
        index += 1        
    result = index
    print(f"part 1: {result}")
    
def part_2(data):
    directions, nodes = data
    current = [node for node in nodes.keys() if node[-1] == "A"]
    print(current)
    index = 0
    result = 0
    while any((node[-1] != "Z" for node in current)):
        direction = directions[index]
        for i in range(len(current)): current[i] = nodes[current[i]][direction]
        index += 1
        result += 1
        if index >= len(directions):
            index = 0
        print(current)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)