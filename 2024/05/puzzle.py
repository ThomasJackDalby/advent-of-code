# Advent Of Code 2024 - Puzzle 5
# https://adventofcode.com/2024/day/5
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2024-12-05 08:22:40.639991

import os
import sys
import requests
from rich import print, traceback
traceback.install()

INPUT_FILE_NAME = "input.txt"
YEAR = 2024
DAY = 5

def get_data():
    if not os.path.exists(INPUT_FILE_NAME):
        session_id = os.environ.get('AOC_SESSION_ID', None)
        if session_id is None: raise Exception("Cannot retrieve input.txt file as session ID is not present in environment variables.")
        data = requests.get(f"https://adventofcode.com/2024/day/5/input", cookies={"session": session_id})
        with open(INPUT_FILE_NAME, "w") as file: file.write(data.text)
    return load_file(INPUT_FILE_NAME if len(sys.argv) < 2 else sys.argv[1])

# --- Solution Start ----
from itertools import groupby

def load_file(file_path):
    def parse_page_order(line):
        return tuple(int(page) for page in line.split("|"))
    
    def parse_book(line):
        return [int(page) for page in line.split(",")]

    with open(file_path, "r") as file: 
        lines = [line.strip() for line in file.readlines()]

    i = lines.index("")
    page_orders = [parse_page_order(line) for line in lines[:i]]
    books = [parse_book(line) for line in lines[i+1:]]
    pre_page_order_map = { group[0] : list(group[1]) for group in groupby(sorted(page_orders, key=lambda page_order: page_order[0]), key=lambda page_order: page_order[0])}
    post_page_order_map = { group[0] : list(group[1]) for group in groupby(sorted(page_orders, key=lambda page_order: page_order[1]), key=lambda page_order: page_order[1])}
    return books, pre_page_order_map, post_page_order_map

def check_order(book, pre_page_order_map, post_page_order_map):
    for i in range(len(book)):
        page = book[i]
        pre_pages = set(book[:i])
        post_pages = set(book[i+1:])
        for page_order in pre_page_order_map.get(page, []):
            if page_order[1] in pre_pages:
                return False
        for page_order in post_page_order_map.get(page, []):
            if page_order[0] in post_pages:
                return False
    return True

def order_book(book, pre_page_order_map, post_page_order_map):
    def check_page(index):
        pre_pages = set(ordered_book[:index])
        post_pages = set(ordered_book[index:])
        for page_order in pre_page_order_map.get(page, []):
            if page_order[1] in pre_pages:
                return False
        for page_order in post_page_order_map.get(page, []):
            if page_order[0] in post_pages:
                return False
        return True
    
    ordered_book = []
    for page in book:
        index = next(i for i in range(len(ordered_book)+1) if check_page(i))
        ordered_book = ordered_book[:index]+[page]+ordered_book[index:]
    return ordered_book

def get_mid_page(book):
    return book[int((len(book)-1)/2)]

def part_1(data):
    books, pre_page_order_map, post_page_order_map = data
    result = sum(get_mid_page(book) 
                 for book in books 
                 if check_order(book, pre_page_order_map, post_page_order_map))
    print(f"part 1: {result}")
    
def part_2(data):
    books, pre_page_order_map, post_page_order_map = data
    result = 0
    for book in books:
        if not check_order(book, pre_page_order_map, post_page_order_map):
            ordered_book = order_book(book, pre_page_order_map, post_page_order_map)
            result += get_mid_page(ordered_book)
    print(f"part 2: {result}")

# --- Solution End ------

if __name__ == "__main__":
    data = get_data()
    part_1(data)
    part_2(data)