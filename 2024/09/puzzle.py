# Advent Of Code 2024 - Puzzle 9
# https://adventofcode.com/2024/day/9
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-10 10:34:49.284612

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 9

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/9/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

import itertools

def load_file(file_path):
    with open(file_path, "r") as file: 
        return file.readline().strip()

def convert_to_files(line):
    files = []
    for file_id, chunk in enumerate(itertools.batched(line, n=2)):  
        file_size = int(chunk[0])
        files.append([file_id, file_size])
        if len(chunk) > 1:
            empty_size = int(chunk[1])
            files.append([-1, empty_size])    
    return files

def convert_to_index(line):
    files = []
    index = 0
    for file_id, chunk in enumerate(itertools.batched(line, n=2)):  
        file_size = int(chunk[0])
        files.append([index, file_id, file_size])
        index += file_size
        if len(chunk) > 1:
            empty_size = int(chunk[1])
            index += empty_size
    return files

def print_disk2(files):
    line = ""
    for index, file in enumerate(files):
        file_index, file_id, file_size = file
        line += str(file_id)*file_size
        if index < len(files)-1:
            line += "." * (files[index+1][0]-(file_index+file_size))
    print(line)

def print_disk1(files):
    line = "".join(("." if file_id == -1 else str(file_id))*file_size for index, file_id, file_size in files)
    print(line)

def calculate_checksum(files):
    # note: works for part2
    checksum = 0
    for file in files:
        file_id, file_size = file[-2], file[-1]
        for i in range(index, index+file_size):
            checksum += file_id * i
        index += file_size
    return checksum

def part_1(data):
    files = convert_to_files(data)

    while True:
        empty_chunk = next((chunk for chunk in files if chunk[0] == -1), None)
        if empty_chunk is None: break

        # this is true as we're filtering out empty space at the end
        # we might need to alter if we change to tracking the empty space instead
        file_chunk = files[-1] 
        delta = empty_chunk[1] - file_chunk[1]

        if delta == 0: ## they fit perfect, just swap them
            empty_chunk[0] = file_chunk[0]
            file_chunk[0] = -1
          
        elif delta > 0: # file is smaller than empty space
            i = files.index(empty_chunk)
            empty_chunk[0] = file_chunk[0]
            empty_chunk[1] = file_chunk[1]
            files.insert(i+1, [-1, delta])
            file_chunk[0] = -1

        else: # file is bigger than empty space    
            empty_chunk[0] = file_chunk[0] # convert empty space to file
            file_chunk[1] = -delta # reduce file size to difference
            
        while files[-1][0] == -1:
            files.pop()

    result = calculate_checksum(files)
    print(f"part 1: {result}")
    
def part_2(data):
    files = convert_to_index(data)
    for file_c in sorted(files, key=lambda file: file[1], reverse=True):
        index = files.index(file_c)
        for i, file_pair in enumerate(zip(files[:index], files[1:index+1])):
            file_a, file_b = file_pair
            empty_size = file_b[0] - (file_a[0] + file_a[2])
            if empty_size < file_c[2]: continue

            files.remove(file_c)
            files.insert(i+1, file_c)
            file_c[0] = file_a[0]+file_a[2]
            break
    result = calculate_checksum(files)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)