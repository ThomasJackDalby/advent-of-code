# Advent Of Code 2023 - Puzzle 4
# https://adventofcode.com/2023/day/4
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-04 14:25:48.367073

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 4

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/4/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

def load_file(file_path):
    def parse_line(line):
        def convert(text_numbers):
            return set(int(number.strip()) for number in text_numbers.strip().split(" ") if len(number) > 0)
        winning_numbers, numbers = (convert(numbers) for numbers in line.strip().split(":")[1].strip().split("|"))
        return (winning_numbers, numbers)

    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def part_1(data):
    total = 0
    for winning_numbers, numbers in data:
        number_of_matches = len(winning_numbers.intersection(numbers))
        result = 0 if number_of_matches == 0 else pow(2, number_of_matches-1)
        total += result

    print(f"part 1: {total}")
    
def part_2(data):
    factors = [1] * len(data)
    for i, (winning_numbers, numbers) in enumerate(data):
        number_of_matches = len(winning_numbers.intersection(numbers))
        factor = factors[i]
        for j in range(0, number_of_matches):
            factors[i+j+1] += factor
    total = sum(factors)
    print(f"part 2: {total}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)