// Advent Of Code 2025 - Puzzle 5
// https://adventofcode.com/2025/day/5
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-07 12:32:33.780174

use std::fs;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    let contents = fs::read_to_string(file_path).unwrap();

    part_1(&contents);
    part_2(&contents);
}

fn part_1(contents: &String) {
    let mut setup_mode = true;
    let mut result: u32 = 0;
    let mut ranges: Vec<(u64, u64)> = Vec::new();

    for line in contents.lines() {
        if setup_mode {
            if line == "" {
                setup_mode = false;
                continue;
            }

            let mut range = line.split("-");
            let start: u64 = range.next().unwrap().parse().unwrap();
            let end: u64 = range.next().unwrap().parse().unwrap();
            ranges.push((start, end));
        }
        else {
            let id: u64 = line.parse().unwrap();
            for (start, end) in ranges.iter() {
                if id >= *start && id <= *end {
                    result += 1;
                    break;
                }
            }
        }
    }
    println!("{result}");
}

fn part_2(contents: &String) {
    let mut ranges: Vec<(u64, u64)> = Vec::new();
    // read all the ranges in the file
    for line in contents.lines() {
        if line == "" {
            break;
        }

        let mut range = line.split("-");
        let start: u64 = range.next().unwrap().parse().unwrap();
        let end: u64 = range.next().unwrap().parse().unwrap();
        ranges.push((start, end));
    }

    // order the ranges by their start value
    ranges.sort_by(|a, b| a.0.cmp(&(b.0)));

    // merge the ranges
    let mut i = 0;
    while i < ranges.len()-1 {
        let mut range_i = ranges[i];
        while i < ranges.len()-1 {
            let range_j = ranges[i+1];        
            match merge_range(range_i, range_j) {
                Some(new_range) => {
                    range_i = new_range;
                    ranges[i] = new_range;
                    ranges.remove(i+1);
                },
                None => {
                    break
                }
            }
        }
        i += 1;
    }

    let mut result: u64 = 0;
    for range in &ranges {
        let range_length = range.1 - range.0 + 1;
        result += range_length;
    }
    println!("{result}");
}

fn merge_range(a: (u64, u64), b: (u64, u64)) -> Option<(u64, u64)> {
    // want to merge ranges into the existing set
    // if they merge, they fully replace the two source ranges

    // if a.0 == b.0 {
    //     if b.1 > a.1 { return Some((a.0, b.1)); } // a0 b0 a1 b1 - a0 b1
    //     return Some((a.0, a.1)); // a0 b0 b1 a1 - a0 a1
    // }

    if a.1 < b.0 || b.1 < a.0 { 
        // a0 a1 b0 b1 - no merge
        // b0 b1 a0 a1 - no merge
        return None
    }
    else if a.0 <= b.0 {
        if b.1 > a.1 { return Some((a.0, b.1)); } // a0 b0 a1 b1 - a0 b1
        return Some((a.0, a.1)); // a0 b0 b1 a1 - a0 a1
    }
    else if b.0 <= a.0 {
        if b.1 > a.1 { return Some((b.0, b.1)); } // b0 a0 a1 b1 - b0 b1
        return Some((b.0, a.1)); // b0 a0 b1 a1 - b0 a1
    }
    else {
        panic!("{} {} vs {} {}", a.0, a.1, b.0, b.1);
    }
}