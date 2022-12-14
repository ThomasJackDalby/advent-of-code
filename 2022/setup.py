
if __name__ == "__main__":

    import sys
    import os

    if len(sys.argv) < 2:
        raise Exception("Puzzle number required")
    number = int(sys.argv[1])

    folder_path = str(number).zfill(2)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    os.chdir(folder_path)
    file = open("input.txt" ,"w")
    file.close()

    import datetime
    lines = [
        f"# Advent Of Code 2022 - Puzzle {number}\n",
        f"# https://adventofcode.com/2022/day/{number}\n",
        "# Tom Dalby - https://github.com/thomasjackdalby\n",
        f"# Date: {datetime.datetime.now()}\n"
        "import sys\n",
        "\n"
        "\n"
        "\n"
        "if __name__ == \"__main__\":\n",
        "    file_path = \"input.txt\" if len(sys.argv) < 2 else sys.argv[1]\n",
        "\n",
        "\n",
        "\n",
    ]

    with open("puzzle.py", "x") as file:
        file.writelines(lines)
