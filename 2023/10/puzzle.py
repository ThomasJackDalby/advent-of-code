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
    
    width = len(lines[0])
    height = len(lines)

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
    return width, height, nodes, lines

def find_main_loop(nodes):
    start = next(filter(lambda n: len(nodes[n])==4, nodes))
    start_links = nodes[start]
    
    for i in range(4):
        current_node = start_links[i]
        previous_node = start
 
        if current_node not in nodes:  continue

        current_node_links = nodes[current_node]
        if start not in current_node_links: continue

        loop = [current_node]
        while len(current_node_links) == 2:
            next_node = current_node_links[0]
            if next_node == previous_node: next_node = current_node_links[1]
            if next_node not in nodes: break
            
            previous_node = current_node
            current_node = next_node
            current_node_links = nodes[current_node]
            if previous_node not in current_node_links: break

            loop.append(current_node)

            if current_node == start: return loop

def part_1(data):
    _, _, nodes, _ = data
    loop = find_main_loop(nodes)
    result = int(len(loop) / 2)
    print(f"part 1: {result}")

UNPROCESSED_TILE = 0
LOOP_TILE = 1
INSIDE_TILE = 2
OUTSIDE_TILE = 3
TILE_STATES = [
    "UNPROCESSED_TILE",
    "LOOP_TILE",
    "INSIDE_TILE",
    "OUTSIDE_TILE",
]

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def part_2(data):
    width, height, nodes, lines = data
    
    def get_index(x, y):
        return y * width + x
    
    loop = find_main_loop(nodes)
    loop_map = [UNPROCESSED_TILE] * width * height
    for node in loop: loop_map[get_index(*node)] = LOOP_TILE

    lx, ly = loop[-2]
    sx, sy = loop[-1]
    fx, fy = loop[0]
    char = None
    if fy==ly: char = "-"
    elif fx==lx: char = "|"
    elif min(fy, ly) < sy:
        if min(fx, lx) < sx: char = "J"
        else: char = "L"
    else:
        if min(fx, lx) < sx: char = "7"
        else: char = "F"
    print(lines[sy])
    lines[sy] = lines[sy][:sx]+char+lines[sy][sx+1:]
    print(lines[sy])
    
    def flood(start, tile_state):
        nonlocal loop_map

        if loop_map[get_index(*start)] != UNPROCESSED_TILE:
            raise Exception()

        queue = [start]
        while len(queue) > 0:
            node = queue.pop(0)
            nx, ny = node
            if loop_map[get_index(nx, ny)] != UNPROCESSED_TILE:
                if loop_map[get_index(nx, ny)] != tile_state: raise Exception(f"{(nx, ny)} is already {loop_map[get_index(nx, ny)]} not {tile_state}")
                continue
            loop_map[get_index(nx, ny)] = tile_state
            for dx, dy in DIRECTIONS:
                x, y = nx + dx, ny + dy
                if x < 0 or x >= width or y < 0 or y >= height: continue
                if loop_map[get_index(x, y)] == UNPROCESSED_TILE:
                    queue.append((x, y))

    def evaluate_tile_type(node):
        x, y = node
        outside_tile = True
        start = None

        while x > 0:
            x -= 1
            tile_state = loop_map[get_index(x, y)]
            if tile_state == INSIDE_TILE: return INSIDE_TILE if outside_tile else OUTSIDE_TILE 
            if tile_state == OUTSIDE_TILE: return OUTSIDE_TILE if outside_tile else INSIDE_TILE 
            if tile_state == LOOP_TILE:
                tile_type = lines[y][x]
                if tile_type == "|": outside_tile = not outside_tile
                elif tile_type == "7" or tile_type == "J": start = tile_type
                elif tile_type == "L" or tile_type == "F":
                    if start is None: raise Exception()
                    if (tile_type == "L" and start == "7") or (tile_type == "F" and start == "J"): outside_tile = not outside_tile
                    start = None
                elif tile_type == "S": raise Exception()
        if start is not None: raise Exception()
        return OUTSIDE_TILE if outside_tile else INSIDE_TILE 

    for x in range(width):
        for y in range(height):
            if loop_map[get_index(x, y)] != UNPROCESSED_TILE: continue
            tile_type = evaluate_tile_type((x, y))
            flood((x, y), tile_type)

    def format(x, y):
        index = get_index(x, y)
        tile_state = loop_map[index]
        # if tile_state == 1: return lines[y][x]
        return "..IO"[tile_state] 
    
    print("##################")
    for y in range(height):
        print("".join((format(x, y) for x in range(width))))
    print("##################")

    result = sum(1 for tile in loop_map if tile == INSIDE_TILE)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)