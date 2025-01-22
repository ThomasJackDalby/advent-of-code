# Advent Of Code 2024 - Puzzle 14
# https://adventofcode.com/2024/day/14
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-17 14:04:25.935927

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 14

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/14/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
    
    def update(self, max_x, max_y):
        self.px += self.vx
        self.py += self.vy
        if self.px < 0: self.px += max_x
        elif self.px >= max_x: self.px -= max_x
        if self.py < 0: self.py += max_y
        elif self.py >= max_y: self.py -= max_y

def load_file(file_path):
    def parse_line(line):
        pos_bit, vel_bit = line.strip().split(" ")
        px, py = [int(x) for x in pos_bit[2:].split(",")]
        vx, vy = [int(x) for x in vel_bit[2:].split(",")]
        return Robot(px, py, vx, vy)

    with open(file_path, "r") as file: 
        return [parse_line(line) for line in file.readlines()]

def part_1(data):
    max_x = 101
    max_y = 103

    for _ in range(100):
        for robot in data:
            robot.update(max_x, max_y)
        
    mid_x = (max_x - 1) / 2
    mid_y = (max_y - 1) / 2
    counts = [0] * 4
    for robot in data:
        if robot.px < mid_x:
            if robot.py < mid_y: counts[0] += 1
            elif robot.py > mid_y: counts[1] += 1
        elif robot.px > mid_x:
            if robot.py < mid_y: counts[2] += 1
            elif robot.py > mid_y: counts[3] += 1

    result = counts[0] * counts[1] * counts[2] * counts[3]
    print(f"part 1: {result}")
    
def part_2(data):

    # at some point they become an xmas tree (after a lot of iterations)
    # hash?
    



    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)