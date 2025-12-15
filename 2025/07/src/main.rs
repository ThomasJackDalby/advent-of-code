// Advent Of Code 2025 - Puzzle 7
// https://adventofcode.com/2025/day/7
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-07 12:31:24.891558

use std::fs;
use std::env;

const START: char = 'S';
const EMPTY: char = '.';
const BEAM: char = '|';
const SPLITTER: char = '^';

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    println!("file_path: {file_path}");

    let contents: Vec<Vec<char>> = fs::read_to_string(file_path)
        .unwrap()
        .lines()
        .map(|line| line.chars().collect::<Vec<char>>())
        .collect();

    println!("{}", part_1(&contents));
    println!("{}", part_2(&contents));
}

fn part_1(contents: &Vec<Vec<char>>) -> u32 {  
    let width: usize = contents[0].len();
    let mut previous_state: Vec<char> = vec![EMPTY; width]; 
    for (i, c) in contents[0].iter().enumerate() {
        if *c == START {
            previous_state[i] = BEAM
        }
    }
    
    let mut result: u32 = 0;
    for line in contents[1..].iter() {
        let mut state: Vec<char> = vec![EMPTY; width]; 
        for x in 0..width {
            if previous_state[x] == BEAM {
                if line[x] == EMPTY { state[x] = BEAM; }
                else if line[x] == SPLITTER {
                    result += 1;
                    if x > 0 { state[x-1] = BEAM; }
                    if x < width-1 { state[x+1] = BEAM; }
                }
            }
        }
        previous_state = state;
    }
    return result;
}

fn part_2(contents: &Vec<Vec<char>>) -> u64 {  
    let width: usize = contents[0].len();
    let mut previous_state: Vec<u64> = vec![0; width]; 
    for (i, c) in contents[0].iter().enumerate() {
        if *c == START {
            previous_state[i] = 1
        }
    }
    
    for line in contents[1..].iter() {
        let mut state: Vec<u64> = vec![0; width]; 
        for x in 0..width {
            let active_beams = previous_state[x];
            if active_beams > 0 {
                if line[x] == EMPTY { state[x] += active_beams; }
                else if line[x] == SPLITTER {
                    if x > 0 { state[x-1] += active_beams; }
                    if x < width-1 { state[x+1] += active_beams; }
                }
            }
        }
        previous_state = state;
    }
    return previous_state.iter().sum();
}