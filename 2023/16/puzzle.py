# Advent Of Code 2023 - Puzzle 16
# https://adventofcode.com/2023/day/16
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-18 21:35:40.412484

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 16

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/16/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return line.strip()

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

next_id = 0
class Beam:
    def __init__(self, x, y, direction):
        global next_id
        self.id = next_id
        self.x = x
        self.y = y
        self.direction = direction
        next_id += 1
    
    def __repr__(self) -> str:
        return f"[{self.id}] ({self.x},{self.y}) {self.direction}"
    
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

# right, up, left, down
DIRECTIONS = [
    (1, 0),
    (0, -1),
    (-1, 0),
    (0, 1),
]

def check(data, sx, sy, direction):
    width = len(data[0])
    height = len(data)

    beams = [ Beam(sx, sy, direction) ]
    energy = [[[False]*4 for _ in range(len(line))] for line in data]

    while len(beams) > 0:
        beam = beams[0]
        dx, dy = DIRECTIONS[beam.direction]
        beam.x += dx
        beam.y += dy

        if beam.x < 0 or beam.x >= width or beam.y < 0 or beam.y >= height:
            beams.pop(0)
            continue

        if energy[beam.y][beam.x][beam.direction]:
            beams.pop(0)
            continue
        energy[beam.y][beam.x][beam.direction] = True

        tile = data[beam.y][beam.x]

        if tile == "/":
            if beam.direction == RIGHT: beam.direction = UP
            elif beam.direction == LEFT: beam.direction = DOWN
            elif beam.direction == DOWN: beam.direction = LEFT
            elif beam.direction == UP: beam.direction = RIGHT
        elif tile == "\\":
            if beam.direction == RIGHT: beam.direction = DOWN
            elif beam.direction == LEFT: beam.direction = UP
            elif beam.direction == DOWN: beam.direction = RIGHT
            elif beam.direction == UP: beam.direction = LEFT
        elif tile == "|":
            if beam.direction in [LEFT, RIGHT]: 
                beams.pop(0)
                beams.append(Beam(beam.x, beam.y, UP))
                beams.append(Beam(beam.x, beam.y, DOWN))
        elif tile == "-":
            if beam.direction in [UP, DOWN]: 
                beams.pop(0)
                beams.append(Beam(beam.x, beam.y, LEFT))
                beams.append(Beam(beam.x, beam.y, RIGHT)) 

    return sum(1 for line in energy for c in line if any(c))

def part_1(data):
    result = check(data, -1, 0, RIGHT)
    print(f"part 1: {result}")
    
def part_2(data):
    width = len(data[0])
    height = len(data)

    result = 0
    for x in range(0, width):
        result = max(result, check(data, x, -1, DOWN))
        result = max(result, check(data, x, height, UP))
    for y in range(0, height):
        result = max(result, check(data, -1, y, RIGHT))
        result = max(result, check(data, width, y, LEFT))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)