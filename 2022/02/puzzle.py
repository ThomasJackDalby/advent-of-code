# Advent Of Code 2022 - Puzzle 2
# https://adventofcode.com/2022/day/2
# Tom Dalby - https://github.com/thomasjackdalby

import sys

file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

# 0 - rock, 1 - paper, 2 - scissors
def get_score(a, b):
    if a == b: # draw, shape + 3
        return 1 + a + 3
    elif (a + 1) % 3 == b: # win, shape + 6
        return 1 + b + 6
    elif (a - 1) % 3 == b: # loss, shape
        return 1 + b
    else:
        raise Exception()

def get_shape_index(value):
    if value == 'A' or value == 'X': return 0
    if value == 'B' or value == 'Y': return 1
    if value == 'C' or value == 'Z': return 2
    raise Exception()

def get_line_score(line):
    a_in, b_in = line.strip().split(" ")
    a = get_shape_index(a_in)
    b = get_shape_index(b_in)
    return get_score(a, b)

with open(file_path, "r") as file:
    lines = file.readlines()

total_score = sum((get_line_score(line) for line in lines))
print("part 1", total_score)

# part 2

def get_line_score_2(line):
    a_in, b_in = line.strip().split(" ")
    a = get_shape_index(a_in)
    if b_in == 'X': # need to lose
        b = (a - 1) % 3
    elif b_in == 'Y': # need to draw
        b = a
    elif b_in == 'Z': # need to win
        b = (a + 1) % 3
    
    return get_score(a, b)

total_score = sum((get_line_score_2(line) for line in lines))
print("part 2", total_score)
