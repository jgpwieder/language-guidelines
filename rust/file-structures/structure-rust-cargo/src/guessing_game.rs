use rand::Rng;
use std::io;
use std::cmp::Ordering;


fn get_string_input() -> String {
    let mut value = String::new(); 
    // This is different from a string literal, it is allocated in the heap
    io::stdin()
        .read_line(&mut value)
        .expect("Failed to read line");
    value.trim().to_string()
    // The function .trim() returns a string slice, .to_string() converts to string
}


pub fn run_guessing_game() {
    println!("Do you want to play a guessing game? (Y/n)");

    let run_game = get_string_input();
    let end_game = String::from("n");
    if run_game == end_game {
        return;
    }

    let secret_number = rand::thread_rng().gen_range(1..=100);
    loop {
        println!("Please input your guess.");
        let guess = get_string_input();
        
        // match function is simply a switch
        let guess: u32 = match guess.parse() { // ": u32" sets the type that the function parse returns from string
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
