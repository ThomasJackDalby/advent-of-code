// Advent Of Code 2025 - Puzzle 3
// https://adventofcode.com/2025/day/3
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-03 21:49:57.117377

use std::fs;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    let contents = fs::read_to_string(file_path).unwrap();
    println!("file_path: {file_path}");

    let mut result: usize = 0;
    for line in contents.lines() {
        result += get_joltage(line);
    }
    println!("{result}");
}

fn get_joltage(batteries: &str) -> usize {
    let mut max_joltage: usize = 0;
    for i in 0..batteries.len() {
        for j in i+1..batteries.len() {
            let joltage_str = [&batteries[i..i+1], &batteries[j..j+1]].concat();
            let joltage = joltage_str.parse().unwrap();
            max_joltage = if joltage > max_joltage { joltage } else { max_joltage };
        }
    }
    return max_joltage;
}