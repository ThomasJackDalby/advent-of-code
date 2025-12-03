use std::env;
use std::fs;

fn main() {
    let file_path = "C:\\Users\\thoma\\source\\repos\\thomasjackdalby\\advent-of-code\\2025\\input.txt";
    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut dial_position: i32 = 50;
    let mut zero_count: u32 = 0;
    for line in contents.lines() {
        let mut value: i32 = line[1..].parse().expect("Should be an int");
        value %= 99;

        if line.starts_with("L") {
            dial_position -= value;
        }
        else {
           dial_position += value; 
        }

        if (dial_position > 99) {
            dial_position -= 99;
        }
        if (dial_position < 0) {
            dial_position += 99;
        }

        if (dial_position == 0) {
            zero_count += 1;
        }
    }
    println!("zero_count: {}", zero_count)
}
