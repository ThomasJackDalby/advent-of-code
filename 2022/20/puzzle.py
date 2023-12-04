# Advent Of Code 2022 - Puzzle 20
# https://adventofcode.com/2022/day/20
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2023-01-05 20:38:42

import sys

def load_file(file_path):
    with open(file_path, "r") as file:
        return [int(line.strip()) for line in file.readlines()]

class LinkedList:

    def __init__(self, values):
        self.nodes = [LinkedList.Node(value, self) for value in values]
        for i, node in enumerate(self.nodes):
            if i > 0:
                previous_node = self.nodes[i-1]
                node.previous = previous_node
                previous_node.next = node
            if i < len(self.nodes)-1:
                next_node = self.nodes[i+1]
                node.next = next_node
                next_node.previous = node

        self.start = self.nodes[0]

        # tie start and end together
        self.nodes[0].previous = self.nodes[-1]
        self.nodes[-1].next = self.nodes[0] 

    def find(self, value):
        return next((node for node in self.nodes if node.value == value), None)

    def enumerate(self):
        node = self.start
        for _ in range(len(self.nodes)):
            yield node.value
            node = node.next

    class Node:

        def __init__(self, value, parent):
            self.parent = parent
            self.previous = None
            self.next = None
            self.value = value

        def remove(self):
            self.next.previous = self.previous
            self.previous.next = self.next
            self.next = None
            self.previous = None

        def get(self, delta):
            if delta == 0:
                return self
            elif delta > 0:
                node = self.next
                for _ in range(abs(delta)-1):
                    node = node.next
                return node
            else:
                node = self.previous
                for _ in range(abs(delta)-1):
                    node = node.previous
                return node

        def __repr__(self):
            return f"<{self.value}>"

        def insert_after(self, node):
            next_node = node.next
            next_node.previous = self
            node.next = self
            self.previous = node
            self.next = next_node

        def move(self, amount):
            if amount == 0: return
            if amount > 0:
                node = self.next
                self.remove()
                node = node.get(amount-1)
                self.insert_after(node)
            else:
                node = self.previous
                self.remove()
                node = node.get(amount+1)
                self.insert_after(node.previous)

def decrypt(data, key=1, rounds=1):
    data = [i * key for i in data]
    number_of_nodes = len(data)

    linked_list = LinkedList(data)
    initial_order = list(linked_list.nodes)

    for _ in range(rounds):
        for node in initial_order:
            node.move(node.value % (number_of_nodes - 1))

    node = linked_list.find(0)
    a = node.get(1000)
    b = a.get(1000)
    c = b.get(1000)
    return a.value + b.value + c.value

if __name__ == "__main__":
    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    data = load_file(file_path)

    # task 1
    print("task 1)", decrypt(data))

    # task 2
    print("task 2)", decrypt(data, 811589153, 10))