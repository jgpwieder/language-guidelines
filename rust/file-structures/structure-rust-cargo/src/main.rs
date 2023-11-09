mod slices;
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
    slices::run_slice_demo();
}
