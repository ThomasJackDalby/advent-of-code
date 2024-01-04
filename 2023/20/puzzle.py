# Advent Of Code 2023 - Puzzle 20
# https://adventofcode.com/2023/day/20
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-24 06:47:01.732485

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 20

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/20/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----
from queue import Queue

DEBUG = False

class Module:
    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

class BroadcastModule(Module):
    def process(self, _, pulse):
        for target in self.targets:
            yield (self.name, target, pulse)

class FlipFlopModule(Module):
    def __init__(self, name, targets):
        self.state = False
        super().__init__(name, targets) 

    def process(self, source, pulse):
        if not pulse: 
            self.state = not self.state
            for target in self.targets:
                yield (self.name, target, self.state)

class ConjunctionModule(Module):
    def __init__(self, name, targets):
        self.sources = {}
        super().__init__(name, targets)
    
    def process(self, source, pulse):
        self.sources[source] = pulse
        pulse = not all(self.sources.values())
        for target in self.targets:
            yield (self.name, target, pulse)

def load_file(file_path):
    def parse_line(line):
        name, targets_part = (part.strip() for part in line.strip().split("->"))
        targets = [target.strip() for target in targets_part.strip().split(",")]
        if name[0] == "%": return FlipFlopModule(name[1:], targets)
        elif name[0] == "&": return ConjunctionModule(name[1:], targets)
        elif name == "broadcaster": return BroadcastModule(name, targets)
        else: raise Exception() 

    with open(file_path, "r") as file:
        modules = { module.name : module for module in (parse_line(line) for line in file.readlines())}

    for module in modules.values():
        for target in module.targets:
            if target in modules:
                target_module = modules[target]
                if isinstance(target_module, ConjunctionModule):
                    target_module.sources[module.name] = False
    if DEBUG:
        for module in modules.values():
            if isinstance(module, ConjunctionModule): print(f"&{module.name} {module.targets} {module.sources}")
            elif isinstance(module, FlipFlopModule): print(f"%{module.name} {module.targets}")
            elif isinstance(module, BroadcastModule): print(f"{module.name} {module.targets}")
    
    return modules

def process(modules, button_press_limit=1000):
    number_of_low_pulses = 0
    number_of_high_pulses = 0
    number_of_button_presses = 0

    rx_found = False
    pulses = Queue()
    while (number_of_button_presses < button_press_limit if button_press_limit is not None else not rx_found):
        pulses.put(("button", "broadcaster", False))
        number_of_button_presses += 1
        while not pulses.empty():
            source, target, pulse = pulses.get()
            if pulse: number_of_high_pulses += 1
            else: number_of_low_pulses += 1
            if DEBUG: print(f"{source} -{('high' if pulse else 'low')}-> {target}")
            if target in modules:
                module = data[target]
                for next_pulse in module.process(source, pulse):
                    if not next_pulse[2] and next_pulse[1] == "rx":
                         print("FOUND!")
                         rx_found = True
                         break
                    pulses.put(next_pulse)
    return number_of_high_pulses, number_of_low_pulses, number_of_button_presses

def part_1(data):
    number_of_high_pulses, number_of_low_pulses, _ = process(data, 1000)
    result = number_of_low_pulses * number_of_high_pulses
    print(f"part 1: {result}")
    
def part_2(data):
    _, _, number_of_button_presses = process(data, None)   
    result = number_of_button_presses
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)