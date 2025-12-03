// Advent Of Code {year} - Puzzle {day}
// https://adventofcode.com/{year}/day/{day}
// Tom Dalby - https://github.com/thomasjackdalby
// Date: {datetime}

use std::fs;
use std::env;

fn main() {{
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 0 {{ &args[1]; }} else {{ "input.txt"; }}
    println!("file_path: {{file_path}}");

    let mut result: u32 = 0;

    println!("{{result}}");
}}