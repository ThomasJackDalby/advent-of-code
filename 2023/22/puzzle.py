# Advent Of Code 2023 - Puzzle 22
# https://adventofcode.com/2023/day/22
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-01-04 06:06:23.148856

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 22

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/22/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def add(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (ax + bx, ay + by, az + bz)

def subtract(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (ax - bx, ay - by, az - bz)

def intersects(a_min, a_max, b_min, b_max):
    if a_max > b_min and a_min < b_max: return True
    if b_max > a_min and b_min < a_max: return True
    return False

class Brick:
    def __init__(self, start, end, key=None) -> None:
        self.key = key
        self.start = start
        self.end = end
        self.size = add(subtract(end, start), (1, 1, 1))

    def move(self, delta):
        start = self.start
        self.start = add(self.start, delta)
        self.end = add(self.end, delta)
        print(f"Moved from {start} to {self.start}")

    def intersects_xy(self, other_brick):
        if not intersects(other_brick.start[0], other_brick.end[0], self.start[0], self.end[0]): return False
        if not intersects(other_brick.start[1], other_brick.end[1], self.start[1], self.end[1]): return False
        return True

    def __repr__(self) -> str:
        return f"{self.start} - {self.end} [{self.size}]"

def display(bricks, axis):
    min_x = min(b.start[axis] for b in bricks)
    max_x = max(b.start[axis] for b in bricks)+1
    max_z = max(b.end[2] for b in bricks)+1
    lines = [[' ' for x in range(min_x, max_x)] for _ in range(max_z)]

    for brick in bricks:
        for z in range(brick.start[2], brick.end[2]+1):
            line = lines[z]
            for x in range(brick.start[axis], brick.end[axis]+1):
                line[x] = brick.key
    for x in range(min_x, max_x): lines[0][x] = "-"
    
    for i, line in enumerate(reversed(lines)):
        print("".join(line)+ f" {max_z-i-1}")
    print()

LETTERS = "ABCDEFGHIJKLMNOPQSTUVWXYZ"
def load_file(file_path):
    def parse_line(line, i):
        start, end = (tuple(int(v) for v in coords.split(",")) for coords in line.strip().split("~"))
        key = LETTERS[i]
        return Brick(start, end, key)

    with open(file_path, "r") as file: return [parse_line(line, i) for i, line in enumerate(file.readlines())]

def part_1(data):

    display(data, 0)
    display(data, 1)

    for brick in sorted(data, key=lambda brick: brick.start[2]):
        lower_bricks = filter(lambda other_brick: other_brick.end[2] <= brick.start[2], data)
        supporting_bricks = filter(lambda other_brick: other_brick.intersects_xy(brick), lower_bricks)
        delta = 1 - max((b.end[2] for b in supporting_bricks), default=1)
        if delta > 0: brick.move((0, 0, delta))

    display(data, 0)
    display(data, 1)

    result = None
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)