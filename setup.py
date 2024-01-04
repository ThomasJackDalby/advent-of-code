# setup.py - Creates folders/boilerplate code for advent-of-code puzzles.
# Tom Dalby - https://github.com/thomasjackdalby

import os
import sys
import datetime
import requests

TEMPLATE_FILE_NAME = "template.txt"
TEMPLATE_FILE_PATH = os.path.join(os.path.dirname(__file__), TEMPLATE_FILE_NAME)
INPUT_FILE_NAME = "input.txt"
TEST_INPUT_FILE_NAME = "test.txt"
SCRIPT_FILE_NAME = "puzzle.py"

def create_blank_file(file_path):
    with open(file_path ,"w") as file:
        pass
    file.close()

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("day", type=int)
    args = parser.parse_args()

    # today = datetime.now()
    # if args.year != today.year:

    folder_path = f"{args.year}/{args.day:02d}"
    if not os.path.exists(folder_path):
        print(f"Creating folders at {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
    os.chdir(folder_path)

    if not os.path.exists(SCRIPT_FILE_NAME):
        print(f"Creating {SCRIPT_FILE_NAME}")
        with open(TEMPLATE_FILE_PATH, "r") as file:
            template = file.read()
        template = template.format(datetime=datetime.datetime.now(), year=args.year, day=args.day)
        with open(SCRIPT_FILE_NAME, "x") as file:
            file.write(template)
    else:
        print("Puzzle file already exists")

    if not os.path.exists(TEST_INPUT_FILE_NAME):
        print(f"Creating {TEST_INPUT_FILE_NAME}")
        create_blank_file(TEST_INPUT_FILE_NAME)

    os.system("cmd")