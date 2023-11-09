mod variables;
mod guessing_game;
 
//  cd /Users/joaowiederkehr/Code/language-guidelines/rust/file-structures/structure-rust-cargo
//  cargo build
//  ./target/debug/rust-test
fn main() {
    let mut i = 0; 
    while i < 10 {
        i = i + 1;
    }
    variables::run_variable_demo();
    guessing_game::run_guessing_game();

    let string = String::from("hello world");
    let word = variables::first_word(&string); // word will get the value 5
    // Keeping track of indexes is not a clean way of doing it, of course you can just create a copy of the values, 
    // but that is not efficient in terms of memory.

    let first_slice = &string[0..word]; // Slices take care of storing that information
    println!("first_slice = {}", first_slice);
    let second_slice = &string[word + 1..];
    println!("second_slice = {}", second_slice);
    // string.clear(); // this empties the String, making it equal to ""
}
