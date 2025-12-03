use std::fs;

const FILE_PATH: &str = "test.txt";

fn main() {
    let contents = fs::read_to_string(FILE_PATH)
        .expect("Should have been able to read the file");
    let mut score: u64 = 0;
    for range in contents.split(",") {
        let values: Vec<&str> = range.split("-").collect();
        let range_start: u64 = values[0].parse().expect("Should parse to int.");
        let range_end: u64 = values[1].parse().expect("Should parse to int.");
        println!("{range_start} {range_end}");

        for id in range_start..range_end+1 {
            if !check_id(id) {
                score += id;
                println!("score: {score}");
            }
        }
    }

    println!("final score: {score}");
}

fn check_id(id: u64) -> bool {       
    let s: String = id.to_string();
    println!("LEN{}", s.len() / 2)
    return false;
    for i in 0..s.len() / 2 {
        for j in 1..(s.len()-i)/2 {
            let first = &s[i..i+j];
            let second = &s[i+j..i+2*j];
            println!("f:{first} s:{second}");
            if first == second {
                println!("{id} {i} {first}");
                return false;
            }
        }
    }
    return true;
}