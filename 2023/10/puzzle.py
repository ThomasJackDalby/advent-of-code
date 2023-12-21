# Advent Of Code 2023 - Puzzle 10
# https://adventofcode.com/2023/day/10
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-10 06:45:17.145503

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 10

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/10/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

TILE_GROUND = "."
NODES = {
    "." : [0, 0, 0, 0],
    "|" : [0, 1, 0, 1],
    "-" : [1, 0, 1, 0],
    "F" : [1, 0, 0, 1],
    "7" : [0, 0, 1, 1],
    "L" : [1, 1, 0, 0],
    "J" : [0, 1, 1, 0],
    "S" : [1, 1, 1, 1],
}
# r u l d
def load_file(file_path):
    with open(file_path, "r") as file: 
        lines = [line.strip() for line in file.readlines()]
    
    nodes = {}
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            node = NODES[tile]
            links = []    
            if node[0] == 1: links.append((x+1, y))
            if node[1] == 1: links.append((x, y-1))
            if node[2] == 1: links.append((x-1, y))
            if node[3] == 1: links.append((x, y+1))
            nodes[(x, y)] = links
    return nodes, lines

def find_main_loop(data, node_callback):
    start = next(filter(lambda n: len(data[n])==4, data))
    start_links = data[start]
    
    for i in range(4):
        valid = True
        current_node = start_links[i]
        previous_node = start
        if current_node not in data: 
            valid = False
            continue

        node_callback(current_node)
        current_node_links = data[current_node]
        while len(current_node_links) == 2:
            next_node = current_node_links[0]
            if next_node == previous_node: next_node = current_node_links[1]
            if next_node not in data:
                valid = False
                break
            
            previous_node = current_node
            current_node = next_node
            current_node_links = data[current_node]
            node_callback(current_node)

        if valid and current_node == start:
            return

def part_1(data):
    nodes, _ = data
    loop_length = 1
    def calculate_loop_length(node):
        nonlocal loop_length
        loop_length += 1

    find_main_loop(nodes, calculate_loop_length)

    result = int(loop_length / 2)
    print(f"part 1: {result}")
    
def part_2(data):
    width = max((x for x, _ in data.keys()))+1
    height = max((y for _, y in data.keys()))+1
    result_map = [0] * width * height
    loop = set()
    def get_index(x, y):
        return y * width + x
    def update(node):
        nonlocal result_map
        result_map[get_index(*node)] = 1
        loop.add[node]
    find_main_loop(data, update)

    for y in range(0, height):
        index = get_index(0, y)
        print("".join("." if i == 0 else "X" for i in result_map[index:index+width]))

    # pick the min x, y loop piece as we know it's edge of loop
    min_loop = None


    # need to flood fill the result map
    start = (0, 0)
    queue = [start]
    while len(queue) > 0:
        pass

    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)