// Advent Of Code 2025 - Puzzle 2
// https://adventofcode.com/2025/day/2
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-03

use std::fs;

fn main() {
    let contents = fs::read_to_string("input.txt").unwrap();
    let mut counter: usize = 0;
    for range in contents.split(",") {
        let mut split_iter = range.split("-");
        let range_start: usize = split_iter.next().unwrap().parse().unwrap();
        let range_end: usize = split_iter.next().unwrap().parse().unwrap();
        for id in range_start..range_end+1 {
            if !check_id(id) {
                counter += id;
            }
        }
    }
    println!("counter: {counter}");
}

fn check_id(id: usize) -> bool {
    let id_str = id.to_string();
    let id_length: usize = id_str.chars().count();
    for pattern_length in 1..(id_length / 2) + 1 {
        if id_length % pattern_length != 0 { 
            continue;
        }
        
        let mut valid: bool = false;
        let left = &id_str[0..pattern_length];
        for i in 1..id_length/pattern_length {
            let right = &id_str[i*pattern_length..(i+1)*pattern_length];
            if left != right {
                valid = true;
                break;
            }
        }
        if !valid {
            return false;
        }
    }
    return true;
}