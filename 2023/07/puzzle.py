# Advent Of Code 2023 - Puzzle 7
# https://adventofcode.com/2023/day/7
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-12-08 13:32:30.258513

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2023
DAY = 7

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2023/day/7/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----

FIVE_OF_A_KIND = 17
FOUR_OF_A_KIND = 13
FULL_HOUSE = 11
THREE_OF_A_KIND = 7
TWO_PAIR = 5
ONE_PAIR = 3
HIGH_CARD = 2

CARD_VALUES = "23456789TJQKA"

def load_file(file_path):
    def parse_line(line):
        hand, bid = line.strip().split(" ")
        return [hand, int(bid)]
    with open(file_path, "r") as file: return [parse_line(line) for line in file.readlines()]

def get_card_type(hand):
    cards = [sum(1 for i in hand if i == c) for c in set(hand)]
    if len(cards) == 1: return FIVE_OF_A_KIND
    if len(cards) == 2: return FOUR_OF_A_KIND if any(filter(lambda c: c == 4, cards)) else FULL_HOUSE
    if len(cards) == 3: return THREE_OF_A_KIND if any(filter(lambda c: c == 3, cards)) else TWO_PAIR
    return ONE_PAIR if len(cards) == 4 else HIGH_CARD

def get_card_rank(hand):
    return sum((v * pow(13, i) for i, v in enumerate(list(map(CARD_VALUES.index, reversed(hand))) + [get_card_type(hand)])))

def part_1(data):
    result = sum(((i + 1) * bid for i, (_, bid) in enumerate(sorted(data, key=lambda game: get_card_rank(game[0])))))
    print(f"part 1: {result}")
    
def part_2(data):
    result = None
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)