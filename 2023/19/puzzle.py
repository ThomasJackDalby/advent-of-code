# Advent Of Code 2023 - Puzzle 19
# https://adventofcode.com/2023/day/19
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-20 06:28:53.528356

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 19

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/19/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

class Rule:
    def __init__(self, target, condition = None, label = None):
        self.target = target
        self.condition = condition if condition is not None else (lambda _: True)
        self.label = label

class Workflow:
    def __init__(self, name, rules):
        self.name = name
        self.rules = rules

    def __repr__(self):
        return f"{self.name}"

class Item:
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
    
    def __repr__(self) -> str:
        return f"x:{self.x} m:{self.m} a:{self.a} s:{self.s}"

def load_file(file_path):
    with open(file_path, "r") as file: 
        lines = [line.strip() for line in file.readlines()]
    
    def parse_rule(text):
        if ":" not in text: return Rule(text, None, text)

        condition, target = text.split(":")
        field = condition[0]
        operator = condition[1]
        value = int(condition[2:])

        if field == "x": condition = (lambda item: item.x > value) if operator == ">" else (lambda item: item.x < value)
        elif field == "m": condition = (lambda item: item.m > value) if operator == ">" else (lambda item: item.m < value)
        elif field == "a": condition = (lambda item: item.a > value) if operator == ">" else (lambda item: item.a < value)
        elif field == "s": condition = (lambda item: item.s > value) if operator == ">" else (lambda item: item.s < value)
        else: raise Exception()
        return Rule(target, condition, text)

    def parse_workflow(line):
        name, rule_parts = line.split("{")
        rules = [parse_rule(w) for w in rule_parts[:-1].split(",")]
        return Workflow(name, rules)

    def parse_item(line):
        line = line[1:-1]
        metrics = [int(part.split("=")[1]) for part in line.split(",")]
        return Item(*metrics)

    i = lines.index("")
    workflows = [parse_workflow(line) for line in lines[:i]]
    items = [parse_item(line) for line in lines[i+1:]]
    return workflows, items

def part_1(data):
    workflows, items = data
    workflows = { workflow.name : workflow for workflow in workflows }
    start_workflow = workflows["in"]

    def process_item(item):
        workflow = start_workflow
        while True:
            for rule in workflow.rules:
                result = rule.condition(item)
                if not result: continue
                if rule.target == "A": return True
                if rule.target == "R": return False
                workflow = workflows[rule.target]
                break

    accepted_items = [item for item in items if process_item(item)]

    result = sum((item.x + item.m + item.a + item.s for item in accepted_items))
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)