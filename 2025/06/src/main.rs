// Advent Of Code 2025 - Puzzle 6
// https://adventofcode.com/2025/day/6
// Tom Dalby - https://github.com/thomasjackdalby
// Date: 2025-12-08 20:06:29.027572

use std::fs;
use std::env;
use regex::Regex;

enum Operator {
    Plus,
    Mult
}

struct Problem {
    values: Vec<u64>,
    operator: Operator
}

impl Problem {
    fn result(&self) -> u64 {
        match self.operator {
            Operator::Mult => self.values.iter().copied().reduce(|a, b| a*b).unwrap(),
            Operator::Plus => self.values.iter().sum(),
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let file_path: &str = if args.len() > 1 { &args[1] } else { "input.txt" };
    println!("file_path: {file_path}");
    let contents = fs::read_to_string(file_path).unwrap();

   part_1(&contents);
   part_2(&contents);
}

fn part_1(contents: &String) {
    let mut problems: Vec<Problem> = Vec::new();
    let mut setup: bool = true; 
    let seperator = Regex::new(r"[ ]+").expect("Invalid regex");
    for line in contents.lines() {
        if setup {
            setup = false;
            for number in seperator.split(line.trim()) {
                let mut problem  = Problem {
                    values: Vec::new(),
                    operator: Operator::Plus,
                };
                problem.values.push(number.parse().unwrap());
                problems.push(problem);
            }
        }
        else {
            let mut i = 0;
            for item in seperator.split(line.trim()) {
                let problem = &mut problems[i];
                match item.parse::<u64>() {
                    Ok(value) => {
                        problem.values.push(value);
                    },
                    Err(_e) => {
                        problem.operator = parse_operator(item);
                    }
                }
                i += 1;
            }
        }
    }

    let result: u64 = problems.iter().map(|problem| problem.result()).sum();
    println!("{result}");
}

fn parse_operator(text: &str) -> Operator {
    return match text {
        "+" => Operator::Plus,
        "*" => Operator::Mult,
        _ => panic!("Ooops"),
    };
}

fn part_2(contents: &String) {
    let lines: Vec::<Vec::<char>> = contents.lines().map(|s| s.chars().collect()) .collect();
    let mut problem_index: usize = 0;
    let index = lines.len()-1;
    let mut result: u64 = 0;
    while problem_index < lines[0].len() {
        let operand = lines[index][problem_index].to_string();
        let mut problem  = Problem {
            values: Vec::new(),
            operator: parse_operator(&operand),
        };

        let mut number_index = 0;
        loop {
            let mut number_chars: Vec::<char> = Vec::new();
            if problem_index+number_index < lines[0].len() {
                for j in 0..index {
                    number_chars.push(lines[j][problem_index+number_index]);
                }
            }
            let number_str: String = number_chars.iter().collect();

            if number_str.trim().is_empty() {
                result += problem.result();
                problem_index += number_index + 1;
                number_index = 0;
                break;
            }
            else {
                let number = number_str.trim().parse().unwrap();
                problem.values.push(number);
            }
            number_index += 1;
        }
    }
    println!("part_2: {}", result);
}