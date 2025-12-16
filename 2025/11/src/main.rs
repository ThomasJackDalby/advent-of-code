// Advent Of Code 2025 - Puzzle 11
// https://adventofcode.com/2025/day/11
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-16 19:33:52.998699

use std::fs;
use std::env;
use itertools::Itertools;
use std::collections::HashMap;

type Id = [char; 3];

const START: Id = ['y', 'o', 'u'];
const OUT: Id = ['o', 'u', 't'];
const SVR: Id = ['s', 'v', 'r'];
const FFT: Id = ['f', 'f', 't'];
const DAC: Id = ['d', 'a', 'c'];

struct Node {
    id: Id,
    children: Vec<Id>
}

fn parse_line(line: &str) -> Node {
    return Node {
        id: line[..3].chars().next_array().unwrap(),
        children: line[5..].split(" ")
            .map(|id| id.chars().next_array().unwrap())
            .collect::<Vec<Id>>()
    };
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    println!("file_path: {file_path}");
    let contents = fs::read_to_string(file_path).unwrap()
        .lines()
        .map(parse_line)
        .collect::<Vec<Node>>();

    println!("part_1: {}", part_1(&contents));
    println!("part_2: {}", part_2(&contents));
}

fn find_node(nodes: &Vec<Node>, node_id: Id) -> &Node {
    return nodes
        .iter()
        .find(|node| node.id == node_id)
        .unwrap();
}

fn count_paths_to_out(nodes: &Vec<Node>, visited: &mut HashMap<(Id, bool, bool), u64>, node_id: &Id, found_dac: bool, found_fft: bool) -> u64 { 
    match visited.get(&(*node_id, found_dac, found_fft)) {
        Some(value) => return *value,
        None => {
            let node = find_node(nodes, *node_id);
            let result = node.children
                .iter()
                .map(|child_id| {
                    match *child_id {
                        OUT => return if found_dac && found_fft { 1 } else { 0 },
                        FFT => return count_paths_to_out(&nodes, visited, child_id, found_dac, true),
                        DAC => return count_paths_to_out(&nodes, visited, child_id, true, found_fft),
                        _ => return count_paths_to_out(&nodes,  visited, child_id, found_dac, found_fft),
                    }
                }).sum();
            visited.insert((*node_id, found_dac, found_fft), result);
            return result;
        }
    }
}

fn part_1(nodes: &Vec<Node>) -> u64 {
    let mut visited = HashMap::new();
    return count_paths_to_out(nodes, &mut visited, &START, true, true);
}

fn part_2(nodes: &Vec<Node>) -> u64 {
    let mut visited = HashMap::new();
    return count_paths_to_out(nodes, &mut visited, &SVR, false, false);
}