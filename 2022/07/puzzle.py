# Advent Of Code 2022 - Puzzle 7
# https://adventofcode.com/2022/day/7
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-12 13:50:19.292908
import sys

class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.folders = []
        self.files = []
        self.parent = parent
        self.size = None

    def get_folders(self):
        return [self] + [sub_folder for folder in self.folders for sub_folder in folder.get_folders()]

    def get_size(self):
        if self.size is None:
            self.size = sum((file.size for file in self.files)) + sum((folder.get_size() for folder in self.folders))
        return self.size

    def get_number_of_files(self):
        return len(self.files) + sum((folder.get_number_of_files() for folder in self.folders))

    def print(self, level=0):
        print(f"{' '*level*4} {self.name} {self.get_size()} {len(self.files)}:{len(self.folders)}")
        for file in self.files:
            print(f"{' '*(level+1)*4} {file.name} {file.size}")
        for folder in self.folders:
            folder.print(level+1)

class File:
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent

def read_input_file(file_path):
    with open(file_path, "r") as file:
        lines = (line.strip() for line in file.readlines())
    
    root = Folder("/")
    current_folder = root

    last_command = None

    while True:
        line = next(lines, None)
        if line is None:
            break
        if line[0] == "$":
            _, command, *args = line.split(" ")
            if command == "cd":
                target_folder_path = args[0]
                if target_folder_path == "..":
                    current_folder = current_folder.parent
                elif target_folder_path == "/":
                    current_folder = root
                else:
                    current_folder = next((folder for folder in current_folder.folders if folder.name == target_folder_path), None)
                if current_folder is None:
                    raise Exception("No current directory")
            last_command = command
        elif last_command == "ls":
            if line.startswith("dir"):
                folder_name = line.split(" ")[1]
                folder = Folder(folder_name, current_folder)
                current_folder.folders.append(folder)
            else:
                size, file_name = line.split(" ")
                file = File(file_name, int(size), current_folder)
                current_folder.files.append(file)

    return root
        
TOTAL_AVAILABLE__DISK_SPACE = 70_000_000
REQUIRED_UNUSED_SPACE = 30_000_000

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    root = read_input_file(file_path)

    folders = root.get_folders()

    # part 1
    small_folders = [folder for folder in folders if folder.get_size() <= 100000]
    total_size = sum(folder.get_size() for folder in small_folders)
    print("part 1", total_size)

    # part 2
    current_size = root.get_size()
    minimal_deletion_size = current_size - (TOTAL_AVAILABLE__DISK_SPACE - REQUIRED_UNUSED_SPACE)

    delete_folders = [folder for folder in folders if folder.get_size() >= minimal_deletion_size]
    delete_folders = list(sorted(delete_folders, key=lambda folder: folder.get_size()))
    print("part 2", delete_folders[0].get_size())
    
        

