# Advent Of Code 2023 - Puzzle 15
# https://adventofcode.com/2023/day/15
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-16 14:37:52.261886

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 15

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/15/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    with open(file_path, "r") as file: 
        return file.readline().strip().split(",")

def hash(text):
    value = 0
    for char in text:
        value += ord(char)
        value *= 17
        value %= 256
    return value

def part_1(data):
    result = sum(hash(step) for step in data)
    print(f"part 1: {result}")
    
def part_2(data):

    boxes = [[] for _ in range(255)]
    for step in data:
        if step[-1].isnumeric():
            label, focus = step[:-2], int(step[-1])
            box_id = hash(label)
            box = boxes[box_id]
            for i in range(len(box)):
                if box[i][0] == label:
                    box[i] = (label, focus)
                    break
            else:
                box.append((label, focus))
        else:
            label = step[:-1]
            box_id = hash(label)
            box = boxes[box_id]
            for i in range(len(box)):
                if box[i][0] == label:
                    boxes[box_id] = box[:i] + box[i+1:]
                    break

    result = sum((i+1) * (j+1) * focus for i in range(len(boxes)) for j, (_, focus) in enumerate(boxes[i]))
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)