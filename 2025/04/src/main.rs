// Advent Of Code 2025 - Puzzle 4
// https://adventofcode.com/2025/day/4
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-04

use std::fs;
use std::env;

const EMPTY: char = '.';
const PAPER: char = '@';
const DELTAS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];

struct Warehouse {
    data: Vec<Vec<char>>,
    width: i32,
    height: i32
}

impl Warehouse {
    fn get(&self, x: i32, y: i32) -> char {
        return self.data[y as usize][x as usize];
    }

    fn remove(&mut self, x: i32, y: i32) {
        self.data[y as usize][x as usize] = EMPTY;
    }

    fn check_access(&self, x: i32, y: i32) -> bool {
        let mut neighbor_count: u32 = 0;
        for (dx, dy) in DELTAS {
            let nx: i32 = x + dx;
            let ny: i32 = y + dy;

            if nx < 0 || nx >= self.width
                || ny < 0 || ny >= self.height { continue; }

            if self.get(nx, ny) == PAPER {
                neighbor_count += 1;
                if neighbor_count >= 4 {
                    return false;
                }
            }
        }
        return true;
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    let contents = fs::read_to_string(file_path).unwrap();
    let data = contents
            .lines()
            .map(|line| line.chars().collect::<Vec<char>>())
            .collect::<Vec<Vec<char>>>();
    let mut warehouse = Warehouse {
        height: data.len() as i32,
        width: data[0].len() as i32,
        data: data,
    };

    println!("width: {}", warehouse.width);
    println!("height: {}", warehouse.height);

    println!("part_1: {}", part_1(&mut warehouse, false));
    println!("part_2: {}", part_2(&mut warehouse));
}

fn part_1(warehouse: &mut Warehouse, remove: bool) -> u32 {
    let mut result: u32 = 0;
    for y in 0..warehouse.height {
        for x in 0..warehouse.width {
            if warehouse.get(x, y) == PAPER {
                if warehouse.check_access(x, y) {
                    if remove { warehouse.remove(x, y); }
                    result += 1;
                }
            }
        }
    }
    return result;
}

fn part_2(warehouse: &mut Warehouse) -> u32 {
    let mut result = 0;
    loop {
        let removed = part_1(warehouse, true);
        if removed == 0 {
            break;
        } 
        result += removed;
    }
    return result;
}
