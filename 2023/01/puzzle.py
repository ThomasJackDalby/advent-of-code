# Advent Of Code 2023 - Puzzle 1
# https://adventofcode.com/2023/day/1
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-01 06:15:01.104691

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 1

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        print("Requesting data")
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/1/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

def load_file(file_path):
    def parse_line(line):
        return line.strip()

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

# --- Solution Start ----

WORDS = { 
    "one" : "1",
    "two" : "2",
    "three" : "3",
    "four" : "4",
    "five" : "5",
    "six" : "6",
    "seven" : "7",
    "eight" : "8",
    "nine" : "9",
}

def part_1(data):
    def parse_line(line):
        numbers = [c for c in line if c.isnumeric()]
        return int(numbers[0]+numbers[-1])

    numbers = sum(parse_line(line) for line in data)
    print(numbers)        

def part_2(data):
    def parse_line(line):
        numbers = []
        i = 0
        while i < len(line):
            c = line[i]
            if c.isnumeric():
                numbers.append(c)
            else:
                for word in WORDS:
                    if len(line) - i < len(word): continue
                    if line[i:i+len(word)] == word:
                        numbers.append(WORDS[word])
                        break
            i += 1
        return int(numbers[0]+numbers[-1])
    
    result = sum(parse_line(line) for line in data)
    print(result)
# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)
