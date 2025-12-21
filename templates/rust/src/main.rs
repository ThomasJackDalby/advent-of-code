// Advent Of Code {year} - Puzzle {day}
// https://adventofcode.com/{year}/day/{day}
// Tom Dalby - https://github.com/thomasjackdalby
// Date: {datetime}

use std::fs;
use std::env;

fn main() {{
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 {{ &args[1] }} else {{ "input.txt" }};
    println!("file_path: {{file_path}}");
    let contents = fs::read_to_string(file_path).unwrap();

    println!("part_1: {{}}", part_1(&contents));
    println!("part_2: {{}}", part_2(&contents));
}}

fn part_1(contents: &str) {{
    let mut result: u32 = 0;
    return result;
}}

fn part_2(contents: &str) {{
    let mut result: u32 = 0;
    return result;
}}