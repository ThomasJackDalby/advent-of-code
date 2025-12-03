# setup.py - Creates folders/boilerplate code for advent-of-code puzzles.
# Tom Dalby - https://github.com/thomasjackdalby

import os
import datetime
from argparse import ArgumentParser

ROOT_FOLDER_PATH = os.path.dirname(__file__)
TEST_FILE_NAME = "test.txt"

def create_blank_file(file_path):
    with open(file_path ,"w") as file:
        pass
    file.close()

def main():
    today = datetime.datetime.now()
    parser = ArgumentParser()
    parser.add_argument("language", type=str)
    parser.add_argument("-y", "--year", type=int, default=today.year)
    parser.add_argument("-d", "--day", type=int, default=today.day)
    args = parser.parse_args()

    print(f"Puzzle {args.year}-{args.day:02d}")

    puzzle_folder_path = os.path.join(ROOT_FOLDER_PATH, f"{args.year}", f"{args.day:02d}")
    if not os.path.exists(puzzle_folder_path):
        print(f"Creating folders at {puzzle_folder_path}")
        os.makedirs(puzzle_folder_path, exist_ok=True)

    # loop over template files
    root_folder_path = os.path.join(ROOT_FOLDER_PATH, "templates", args.language)
    for folder_path, _, file_names in os.walk(root_folder_path):
        target_folder_path = os.path.join(puzzle_folder_path, os.path.relpath(folder_path, root_folder_path))
        if not os.path.exists(target_folder_path):
            print(f"Creating directory [{target_folder_path}]")
            os.makedirs(target_folder_path, exist_ok=True)

        for file_name in file_names:
            source_file_path = os.path.join(folder_path, file_name)
            file_path = os.path.relpath(source_file_path, root_folder_path)
            target_file_path = os.path.join(puzzle_folder_path, file_path)

            if not os.path.exists(target_file_path):
                print(f"Creating file [{target_file_path}]")
                with open(source_file_path, "r") as file:
                    template = file.read()
                template = template.format(datetime=datetime.datetime.now(), year=args.year, day=args.day)
                with open(target_file_path, "x") as file:
                    file.write(template)
            else:
                print(f"Template [{file_path}] already exists.")

    test_target_file_path = os.path.join(puzzle_folder_path, TEST_FILE_NAME)
    if not os.path.exists(test_target_file_path):
        create_blank_file(test_target_file_path)

    # os.system("cmd")

if __name__ == "__main__":
    main()