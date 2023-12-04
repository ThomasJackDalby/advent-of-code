# Advent Of Code 2022 - Puzzle 19
# https://adventofcode.com/2022/day/19
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-01-04 18:50:29.284134
import sys
import regex
import random

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [[int(n) for n in regex.findall("-?\d+", line)] for line in file.readlines()]
        return [[[a,0,0], [b,0,0], [c,d,0], [e,0,f]] for i, a, b, c, d, e, f in lines]

def evaluate(recipes, recipe_index, start_time, resources, robots):
    for t in range(start_time, 24):
        print(f"{t:2} | {' '.join((f'{r:3}' for r in resources))} |{' '.join((f'{r:3}' for r in robots))}")

        recipe = recipes[recipe_index]
        can_build = True
        for i in range(len(recipe)):
            if resources[i] < recipe[i]:
                can_build = False
                break
        if can_build:
            for i in range(len(recipe)):
                resources[i] -= recipe[i]
                              
        # collect resources
        for i in range(4):
            resources[i] += robots[i]
        
        # finish building
        if can_build:
            robots[recipe_index] += 1

            # return max of next
            return max((evaluate(recipes, i, t+1, list(resources), list(robots)) for i in range(4)))

    return resources[-1]    

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]

    blue_prints = load_file(file_path)
    
    resources = [0] * 4
    robots = [0] * 4
    
    # we start with 1 ore robot
    robots[0] = 1
    order_index = 0

    result = max((evaluate(blue_prints[0], i, 0, list(resources), list(robots)) for i in range(4)))