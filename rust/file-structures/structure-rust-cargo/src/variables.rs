

fn pass_value(a_string: String) -> String {
    a_string
}


fn pass_reference(_a_string: & String) {
}


fn pass_mutable_reference(a_string: &mut String) {
    a_string.push_str(" - mutated");
}


pub fn run_variable_demo() {
    let string_literal = "Hello"; // Simple type -> stack -> passed as val
    let mut string = String::from(string_literal); // Complex type -> heap -> passed as ref
    string.push_str(", world!");

    println!("string_literal = {}", string_literal);
    println!("string = {}", string);
    
    // -> COPYING VARIABLES
    let string1 = string.clone();
    println!("string1 = {}", string1);
    println!("string = {}", string);

    let string2 = string;
    println!("string2 = {}", string2);
    // println!("string = {}", string); -> This generates an error for varaibles that are not simple (in stack) due to Note1

    // -> PASSING VARIABLE TO FUNCTION
    pass_value(string1); 
    // println!("string1 = {}", string1); -> This generates an error because heap is freed when variable is returned due to Note2

    let string3 = pass_value(string2); // Tedious to have to return passed values everytime
    println!("string3 = {}", string3);

    pass_reference(&string3); // Can pass as refference with &
    println!("string3 = {}", string3);

    let mut string3 = String::from(string_literal); // -> heap -> passed as mutable reference, MAKES IT SO CLEAR THAT IT WILL CHANGE IT
    let string3_ref1 = &mut string3;
    // let _string3_ref2 = &mut string3; //-> Cannot have 2 mutable references to the same variable with scopes that coexist. Prevents data races
    // println!("r2: {}, r3: {}", string3_ref1, _string3_ref2); -> Needed for error since the scope of the reference goes untill the last time it was used

    pass_mutable_reference(string3_ref1);
    println!("string3 = {}", string3);
    let _string3_ref2 = &mut string3; // After inactivated by called function ending you can have another mutable reference
    // let _string3_ref3 = & string3; //-> Also cannot have mutable and immutable references to the same variable -> prevents dangling references (pointers to values that were freed)
    // println!("r2: {}, r3: {}", _string3_ref2, _string3_ref3);
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
