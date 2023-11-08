mod my_lib;


fn pass_value(a_string: String) -> String {
    a_string
}


fn pass_reference(a_string: &mut String) {
    a_string.push_str(" - mutated");
}


fn main() {
    let string_literal = "Hello"; // Simple type -> stack -> passed as val
    let mut string = String::from(string_literal); // Complex type -> heap -> passed as ref
    string.push_str(", world!");

    println!("string_literal = {}", string_literal);
    println!("string = {}", string);
    
    let string1 = string.clone();
    println!("string1 = {}", string1);
    println!("string = {}", string);

    let string2 = string;
    println!("string2 = {}", string2);
    // println!("string = {}", string); -> This generates an error for varaibles that are not simple (in stack) due to Note1

    let string3 = pass_value(string1);
    // println!("string1 = {}", string1); -> This generates an error because heap is freed when variable is returned due to Note2
    println!("string3 = {}", string3);

    let string3 = pass_value(string3); // Tedious to do this to every variable, can pass as refference with &
    println!("string3 = {}", string3);

    let mut string3 = String::from(string_literal); // Complex type -> heap -> passed as mutable reference, SO CLEAR THAT IT WILL CHANGE IT
    let string3_ref1 = &mut string3;
    // let _string3_ref2 = &mut string3; -> Cannot have 2 mutable references active. Prevents data races
    pass_reference(string3_ref1);
    println!("string3 = {}", string3);
    let _string3_ref2 = &mut string3; // After inactivated by called function ending you can

    let mut i = 0;
    while i < 10 {
        println!("hello: {}", i);
        i = i + 1;
    }

    my_lib::run();
}

// Notes:
// RUST WILL NEVER CREATE DEEP COPIES OD DATA!
// - Note1: 
//   Rust clears the values in the stack for a variable when that veriable 
//   runs out of scope (End of function where it was defined). If String type
//   variables are passed as reference this is dangerous. To solve that, once a 
//   value is copied by reference, the previous variable become invalid.
// - Note2:
//   Passing a variable to a function is the exact same as making a copy,
//   meaning complex variables are invalidated when passed as arguments
//   because the scope ends when the function ends.