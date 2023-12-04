# Advent Of Code 2022 - Puzzle 13
# https://adventofcode.com/2022/day/13
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-19 10:13:19.065040
import sys
import functools

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        
    patterns = []
    for line in lines:
        if line == "": continue

        number = ""
        stack = []
        root = None
        for c in line:
            if c == "[":
                stack.append([])
                if len(stack) > 1:
                    stack[-2].append(stack[-1])
            elif c == "]":
                if number != "":
                    stack[-1].append(int(number))
                number = ""
                root = stack.pop()
            elif c == ",":
                if number != "":
                    stack[-1].append(int(number))
                number = ""
            else:
                number += c
        patterns.append(root)
    return patterns

def compare_integers(left, right):
    if left < right: return -1
    elif left > right: return 1
    else: return 0

def compare_lists(left, right):
    max_length = len(left) if len(left) > len(right) else len(right)
    for i in range(max_length):
        if i < len(left) and i < len(right):
            result = compare(left[i], right[i])
            if result != 0: return result
        elif i >= len(left): return -1
        elif i >= len(right): return 1
        else: raise Exception()
    return 0

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int): return compare_integers(left, right)
    elif isinstance(left, list) and isinstance(right, list): return compare_lists(left, right)
    elif isinstance(left, int): return compare_lists([left], right)
    elif isinstance(right, int): return compare_lists(left, [right])
    else: raise Exception()

def part_1(patterns):
    total = 0
    for i, left, right in ((i, patterns[i], patterns[i+1]) for i in range(0, len(patterns), 2)):
        index = i // 2 + 1
        result = compare(left, right)
        if result == -1:
            total += index
    return total

def part_2(patterns):
    div_1 = [[2]]
    div_2 = [[6]]
    patterns.append(div_1)
    patterns.append(div_2)
    patterns.sort(key=functools.cmp_to_key(compare))
    a = (patterns.index(div_1) + 1)
    b = (patterns.index(div_2) + 1)
    return a * b

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    patterns = load_file(file_path)
    p1 = part_1(patterns)
    print("part_1", p1)

    p2 = part_2(patterns)
    print("part_2", p2)
