mod variables;
mod guessing_game;


fn main() {
    let mut i = 0; 
    while i < 10 {
        i = i + 1;
    }
    variables::run_variable_demo();
    guessing_game::run_guessing_game();
}
