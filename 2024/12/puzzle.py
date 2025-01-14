# Advent Of Code 2024 - Puzzle 12
# https://adventofcode.com/2024/day/12
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-13 19:30:11.390509

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 12

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/12/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        return [c for c in line.strip()]

    with open(file_path, "r") as file: 
        return [parse_line(line) for line in file.readlines()]

EMPTY = "."

def part_1(data):
    width = len(data[0]) 
    height = len(data) 
    result = 0

    for sy in range(height):
        for sx in range(width):
            region_type = data[sy][sx]
            if region_type == EMPTY: continue

            queue = [(sx, sy)]
            region = set([(sx, sy)])
            perimeter = 0

            def check_and_add_neighbour(x, y):
                nonlocal perimeter
                if x < 0 or x >= width: return
                if y < 0 or y >= height: return
                if data[y][x] != region_type: return
                perimeter -= 1
                if (x, y) in region: return
                queue.append((x, y))
                region.add((x, y))

            while len(queue) > 0:
                tx, ty = queue.pop()
                perimeter += 4

                check_and_add_neighbour(tx-1, ty)
                check_and_add_neighbour(tx+1, ty)
                check_and_add_neighbour(tx, ty-1)
                check_and_add_neighbour(tx, ty+1)
            
            for tx, ty in region:
                data[ty][tx] = EMPTY

            area = len(region)
            cost = area * perimeter
            result += cost

    print(f"part 1: {result}")

def find_regions(data):
    width = len(data[0])
    height = len(data)
    regions = set()

    for sy in range(height):
        for sx in range(width):
            region_type = data[sy][sx]
            if (sx, sy) in regions: continue

            queue = [(sx, sy)]
            region = set([(sx, sy)])

            def check_and_add_neighbour(x, y):
                if x < 0 or x >= width: return
                if y < 0 or y >= height: return
                if data[y][x] != region_type: return
                if (x, y) in region: return
                queue.append((x, y))
                region.add((x, y))

            while len(queue) > 0:
                tx, ty = queue.pop()
                check_and_add_neighbour(tx-1, ty)
                check_and_add_neighbour(tx+1, ty)
                check_and_add_neighbour(tx, ty-1)
                check_and_add_neighbour(tx, ty+1)
            
            regions.update(region)
            print(f"Found [{region_type}] of size {len(region)}.")
            yield region

def part_2(data):
    result = 0

    # detect all regions using part 1 method
    # treating regions individually, loop over rows and columns, detecting continuous edges
    regions = find_regions(data)
    for region in regions:
        # get the extent of the region (to avoid looping over unecessary tiles)
        min_x = min(x for x, _ in region)
        max_x = max(x for x, _ in region)
        min_y = min(y for _, y in region)
        max_y = max(y for _, y in region)

        number_of_edges = 0

        for y in range(min_y, max_y + 1):
            for dy in [-1, 1]:
                edge_started = False
                for x in range(min_x, max_x + 2):
                    if not edge_started and (x, y) in region and (x, y + dy) not in region: # we've not started an edge, we're in the region and we are an edge so start
                        edge_started = True
                    elif edge_started and ((x, y) not in region or (x, y + dy) in region): # we are at the end of an edge
                        edge_started = False
                        number_of_edges += 1
        
        for x in range(min_x, max_x + 1):
            for dx in [-1, 1]:
                edge_started = False
                for y in range(min_y, max_y + 2):
                    if not edge_started and (x, y) in region and (x + dx, y) not in region:
                        edge_started = True
                    elif edge_started and ((x, y) not in region or (x + dx, y) in region):
                        edge_started = False
                        number_of_edges += 1
        
        area = len(region)
        cost = area * number_of_edges
        result += cost

    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
   # part_1(data)
    part_2(data)