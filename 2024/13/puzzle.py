# Advent Of Code 2024 - Puzzle 13
# https://adventofcode.com/2024/day/13
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-15 10:11:25.776912

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 13

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/13/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

import re

SEARCH_PATTERN = r"Button A: X\+([0-9]+), Y\+([0-9]+)\nButton B: X\+([0-9]+), Y\+([0-9]+)\nPrize: X=([0-9]+), Y=([0-9]+)"

def load_file(file_path):
    with open(file_path, "r") as file: 
        file_contents = "".join(file.readlines())

    return [tuple(int(x) for x in game) for game in re.findall(SEARCH_PATTERN, file_contents)]

def part_1(data):

    def solve_claw_machine(game):
        ax, ay, bx, by, px, py = game
        x, y = 0, 0
        a_count = 0     
        while x < px and y < py and a_count < 100:
            x += ax
            y += ay
            a_count += 1
            b_count_dx = (px - x) / bx
            b_count_dy = (py - y) / by
            if b_count_dx != int(b_count_dx) or b_count_dy != int(b_count_dy): continue

            b_count_dx = int(b_count_dx)
            b_count_dy = int(b_count_dy)
            if b_count_dx != b_count_dy: continue 

            b_count = int(b_count_dx)
            if b_count > 100: continue
                
            tokens = 3 * a_count + b_count
            return tokens
        return None

    print(f"There are {len(data)} games")
    result = 0
    solved_games = 0
    for game in data:
        tokens = solve_claw_machine(game)
        if tokens != None:
            result += tokens
            solved_games += 1

    print(f"{solved_games} solved games.")
    print(f"part 1: {result}")
    
def part_2(data):
    def solve_claw_machine(game):
        ax, ay, bx, by, px, py = game
        
        px += 10000000000000
        py += 10000000000000

        # can we put the lines equal to each other
        # y = mx + c
        # y = (dy)/(dx)x + c
        # ax/ay goes through zero

        # y = ay/ax x 
        # py = by/bx px + C   
        # C = py - bx*px/by

        # so a point exists if we can solve
        # ay/ax x = by/bx x + py/px bx/by
        # x = py/px * bx/by / (ay/ax - by/bx)

        def find_x():
            return ((py / px) * (bx / by)) / ((ay / ax) - (by / bx))
        
        int_x = find_x()


    print(f"There are {len(data)} games")
    result = 0
    solved_games = 0
    for game in data:
        tokens = solve_claw_machine(game)
        if tokens != None:
            result += tokens
            solved_games += 1

    print(f"{solved_games} solved games.")
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)