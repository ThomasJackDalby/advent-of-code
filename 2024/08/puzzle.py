# Advent Of Code 2024 - Puzzle 8
# https://adventofcode.com/2024/day/8
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-09 18:51:15.010088

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 8

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/8/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

import itertools

def load_file(file_path):
    with open(file_path, "r") as file: 
        lines = [line.strip() for line in file.readlines()]
    width = len(lines[0])
    height = len(lines)
    antennas = {}
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == ".": continue
            if value not in antennas: antennas[value] = set()
            antennas[value].add((x, y))
    return width, height, antennas

def in_limits(x, y, width, height):
    return x >= 0 and y >= 0 and x < width and y < height

def add_antinode(locations, width, height, x, y, dx, dy, include_reflections=False):
    if include_reflections:
        locations.add((x, y))
    x -= dx
    y -= dy
    while in_limits(x, y, width, height):
        locations.add((x, y))
        x -= dx
        y -= dy
        if not include_reflections:
            return

def add_antinodes(locations, width, height, antenna_a, antenna_b, include_reflections = False):
    ax, ay = antenna_a
    bx, by = antenna_b
    add_antinode(locations, width, height, ax, ay, bx - ax, by - ay, include_reflections)
    add_antinode(locations, width, height, bx, by, ax - bx, ay - by, include_reflections)

def part_1(data):
    width, height, antennas = data
    locations = set()
    for antenna_locations in antennas.values():
        for antenna_a, antenna_b in itertools.combinations(antenna_locations, 2):
            add_antinodes(locations, width, height, antenna_a, antenna_b)
    result = len(locations)
    print(f"part 1: {result}")
    
def part_2(data):
    width, height, antennas = data
    locations = set()
    for antenna_locations in antennas.values():
        for antenna_a, antenna_b in itertools.combinations(antenna_locations, 2):
            add_antinodes(locations, width, height, antenna_a, antenna_b, True)
    result = len(locations)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)