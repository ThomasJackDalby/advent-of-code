# Advent Of Code 2022 - Puzzle 3
# https://adventofcode.com/2022/day/3
# Tom Dalby - https://github.com/thomasjackdalby

import sys

file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

def get_priority(item_type):
    v = ord(item_type)
    if v >= 97:
        return v - 97 + 1
    else:
        return v - 65 + 26 + 1

with open(file_path, "r") as file:
    lines = [line.strip() for line in file.readlines()]

def find_duplicate_item(line):
    half_length = len(line)//2 
    left = set(line[:half_length])
    right = set(line[half_length:])
    item_type = next(iter(left & right))
    return get_priority(item_type)

score = sum((find_duplicate_item(line) for line in lines))
print("part 1", score)

def read_groups(lines):
    for i in range(0, len(lines), 3):
        yield lines[i:i + 3]

def find_badge_id(group):
    a = set(group[0])
    b = set(group[1])
    c = set(group[2])

    item_type = next(iter(a & b & c))
    return get_priority(item_type)

score = sum((find_badge_id(group) for group in read_groups(lines)))
print("part 2", score)
