# Advent Of Code 2022 - Puzzle 11
# https://adventofcode.com/2022/day/11
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-15 13:01:42.911546
import sys
from math import trunc

monkeys = []

class Monkey:
    def __init__(self, lines) -> None:
        self.total_items_inspected = 0
        self.monkey_id = lines[0].split(" ")[1].rstrip(":").strip()
        self.items = [int(item.strip()) for item in lines[1].split(":")[1].strip().split(",")]
        self.inspect = parse_operand(lines[2].split(":")[1].strip())
        self.factor = int(lines[3].split(" ")[-1])
        self.targets = {}
        self.target_ids = {
            True: int(lines[4].split(" ")[-1]),
            False: int(lines[5].split(" ")[-1])
        }

    def process(self):
        for item in self.items:
            for i, factor in enumerate(self.factors):
                item[i] = self.inspect(item[i]) % factor
            result = item[self.factor_index] == 0
            self.targets[result].items.append(item)
            self.total_items_inspected += 1
        self.items = []

    def process_old(self):
        for item in self.items:
            item = self.inspect(item)
            item = trunc(item / 3.0)
            result = item % self.factor == 0
            self.targets[result].items.append(item)
            self.total_items_inspected += 1
        self.items = []

def parse_operand(text):
    _, operator, argB = text.split("=")[1].strip().split(" ")
    if argB == "old":
        return lambda old: old ** 2
    argB = int(argB)
    if operator == "*":
        return lambda old: old * argB
    if operator == "+":
        return lambda old: old + argB
    raise Exception()

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    i = 0
    monkeys = []
    while 7*i < len(lines):
        monkey = Monkey(lines[7*i:7*i+7])
        monkeys.append(monkey)
        i += 1

    for monkey in monkeys:
        monkey.targets[True] = monkeys[monkey.target_ids[True]]
        monkey.targets[False] = monkeys[monkey.target_ids[False]]

    return monkeys

def part_1(file_path):
    monkeys = load_file(file_path)

    for r in range(10000):
        for monkey in monkeys:
            monkey.process()

    monkeys.sort(key=lambda monkey: -monkey.total_items_inspected)
    monkey_business = monkeys[0].total_items_inspected * monkeys[1].total_items_inspected
    print("part 1", monkey_business)
    for monkey in monkeys:
        print(monkey.monkey_id, monkey.total_items_inspected)

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    monkeys = load_file(file_path)

    factors = [monkey.factor for monkey in monkeys]
    def convert_to_factor_list(item):
        return [item % factor for factor in factors]
    for monkey in monkeys:
        monkey.factors = factors
        monkey.factor_index = factors.index(monkey.factor)
        monkey.items = [convert_to_factor_list(item) for item in monkey.items]

    for r in range(10000):
        for monkey in monkeys:
            monkey.process()

    monkeys.sort(key=lambda monkey: -monkey.total_items_inspected)
    monkey_business = monkeys[0].total_items_inspected * monkeys[1].total_items_inspected
    print("part 1", monkey_business)
    for monkey in monkeys:
        print(monkey.monkey_id, monkey.total_items_inspected)
