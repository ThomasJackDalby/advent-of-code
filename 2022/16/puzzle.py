# Advent Of Code 2022 - Puzzle 16
# https://adventofcode.com/2022/day/16
# Tom Dalby - https://github.com/thomasjackdalby
# Date: 2022-12-23 12:28:37.961923
import sys

ID_OFFSET = len("Valve ")
FLOWRATE_OFFSET = len("Valve AA has flow rate=")
LINKED_IDS_OFFSET = len(" tunnels lead to valve ")

class Valve:
    def __init__(self, valve_index, valve_id, flow_rate, linked_valve_ids):
        self.valve_index = valve_index
        self.valve_id = valve_id
        self.flow_rate = flow_rate
        self.linked_valve_ids = linked_valve_ids
    
    def __repr__(self) -> str:
        return self.valve_id

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    valves = []
    for valve_index, line in enumerate(lines):
        prefix, suffix = line.split(";")
        valve_id = prefix[ID_OFFSET:ID_OFFSET+2]
        flow_rate = int(prefix[FLOWRATE_OFFSET:])
        linked_valve_ids = [id.strip() for id in suffix[LINKED_IDS_OFFSET:].split(",")]
        valves.append(Valve(valve_index, valve_id, flow_rate, linked_valve_ids))
    for valve in valves:
        valve.linked_valves = [next(valve for valve in valves if valve.valve_id == linked_valve_id) for linked_valve_id in valve.linked_valve_ids]
    return valves

def get_distance(start_node_index, target_node_index, nodes):
    distances = [None] * len(nodes)
    distances[start_node_index] = 0
    queue = [start_node_index]
    while len(queue) > 0:
        node_index = queue.pop(0)
        node = nodes[node_index]
        next_distance = distances[node_index] + 1
        for linked_valve in node.linked_valves:
            if distances[linked_valve.valve_index] is None or next_distance < distances[linked_valve.valve_index]:
                queue.append(linked_valve.valve_index)
                distances[linked_valve.valve_index] = next_distance
    
    node_index = target_node_index
    distance = 0
    while node_index != start_node_index:
        node = nodes[node_index]
        min_distance = None
        min_index = None
        for linked_valve in node.linked_valves:
            if min_distance is None or distances[linked_valve.valve_index] < min_distance:
                min_distance = distances[linked_valve.valve_index]
                min_index = linked_valve.valve_index
        node_index = min_index
        distance += 1

    return distance

def search(valves, time_out, current_valve_index, state, filtered_valves=None, cache = None):
    
    def should_visit_valve(valve):
        if valve.flow_rate == 0: return False
        if state[valve.valve_index]: return False
        if filtered_valves is not None and valve.valve_id not in filtered_valves: return False
        return True

    remaining_valves_state = [should_visit_valve(valve) for valve in valves]
    remaining_valves = [valves[valve_index] for valve_index, valve_state in enumerate(remaining_valves_state) if valve_state]
    if len(remaining_valves) == 0:
        return 0 

    # cache the remaining valve states
    if cache is None:
        cache = {}
    hash_code = hash(tuple([current_valve_index, time_out] + remaining_valves_state))
    if hash_code in cache:
        return cache[hash_code]

    max_pressure = 0
    for target_valve in remaining_valves:
        distance = get_distance(current_valve_index, target_valve.valve_index, valves)
        
        target_valve_time_out = time_out - (distance + 1) # time to get there and open it
        if target_valve_time_out <= 0:
            continue

        target_valve_pressure = target_valve_time_out * target_valve.flow_rate
        target_valve_state = state.copy()
        target_valve_state[target_valve.valve_index] = True
        pressure = target_valve_pressure + search(valves, target_valve_time_out, target_valve.valve_index, target_valve_state, filtered_valves, cache)
        max_pressure = max(max_pressure, pressure)
    
    cache[hash_code] = max_pressure
    return max_pressure

def part_1(valves, time_out = 30):
    start_valve_index = next(v.valve_index for v in valves if v.valve_id == "AA")
    return search(valves, time_out, start_valve_index, [False]*len(valves))

def get_combinations(elements, n):
    if n == 1: 
        return [[a] for a in elements]
    return [[a] + b for i, a in enumerate(elements) 
                    for b in get_combinations(elements[i+1:], n-1)]  

def get_groups(elements):
    group_sizes = [(i, len(elements) - i) for i in range(1, 1 + len(elements) // 2)]
    for group_size in group_sizes:
        combinations = get_combinations(elements, group_size[0])
        if group_size[0] == group_size[1]:
            combinations = combinations[:len(combinations) // 2]
        for left in combinations:
            right = list(elements)
            for element in left:
                right.remove(element)
            yield [left, right]

def part_2(valves, time_out = 26):
    start_valve_index = next(v.valve_index for v in valves if v.valve_id == "AA")

    # only interested in traveling to active valves
    active_valves = [valve for valve in valves if valve.flow_rate > 0]
    cache = {}
    max_pressure = 0
    for group_a, group_b in get_groups([valve.valve_id for valve in active_valves]):
        # print(group_a, group_b)
        result_a = search(valves, time_out, start_valve_index, [False]*len(valves), group_a, cache)
        result_b = search(valves, time_out, start_valve_index, [False]*len(valves), group_b, cache)
        result = result_a + result_b
        print(",".join(group_a), ",".join(group_b), result, max_pressure)
        max_pressure = max(max_pressure, result)
    return max_pressure

if __name__ == "__main__":

    file_path = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
    valves = load_file(file_path)

    print("part_1:", part_1(valves))
    print("part_2:", part_2(valves))
