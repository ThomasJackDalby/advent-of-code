use std::fs;

const FILE_PATH: &str = "input.txt";
const DIAL_SIZE: i32 = 100;
const DIAL_START: i32 = 50;

fn main() {
    let contents = fs::read_to_string(FILE_PATH)
        .expect("Should be able to read the file.");

    let mut counter: i32 = 0;
    let mut dial_value: i32 = DIAL_START;

    for line in contents.lines() {
        // parse the integer value from the line
        // L means minus
        let mut value: i32 = line[1..].parse().expect("Integer should be parsable.");
        if line.starts_with("L") { value *= -1; }

        let counter_increment: i32;
        (dial_value, counter_increment) = process_line(dial_value, value);

        counter += counter_increment;
    }

    println!("counter={counter}");
}

fn process_line(mut dial_value: i32, value: i32) -> (i32, i32) {
    // split the value up into how many revolutions
    let divisor = value / DIAL_SIZE;
    let remainder = value % DIAL_SIZE;
    let mut counter = divisor.abs();
    
    dial_value += remainder;

    if dial_value < 0 {
        if dial_value != remainder { counter += 1; }
        dial_value += DIAL_SIZE;
    }
    else if dial_value == 0 {
        counter += 1;
    }
    else if dial_value >= DIAL_SIZE {
        dial_value -= DIAL_SIZE;
        counter += 1;
    }

    return (dial_value, counter);
}


macro_rules! line_tests {
    ($($name:ident: $value:expr,)*) => {
    $(
        #[test]
        fn $name() {

            let (in_dial_value, in_value, out_dial_value, out_counter_inc) = $value;
            let dial_value: i32; 
            let counter_inc: i32; 
            
            (dial_value, counter_inc) = process_line(in_dial_value, in_value);

            assert_eq!(dial_value, out_dial_value);
            assert_eq!(counter_inc, out_counter_inc);
        }
    )*
    }
}

line_tests! {
    fib_1: (0, 10, 10, 0),
    fib_2: (10, 100, 10, 1),
    fib_3: (10, 200, 10, 2),
    fib_4: (10, 190, 0, 2),
    fib_5: (10, -110, 0, 2),
    fib_6: (10, -15, 95, 1),
    fib_7: (10, -10, 0, 1),
    fib_8: (0, -10, 90, 0),
}