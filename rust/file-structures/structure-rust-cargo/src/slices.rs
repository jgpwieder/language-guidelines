

pub fn run_slice_demo() {
    // Lets say you want to get the first occurance of a word
    let string = String::from("hello world");
    let word = first_word_index(&string); 
    // Without a propper data type, wwe must deal with idexes.
    // Keeping track of indexes is not a clean way of doing it, if the reference changes 
    // (like cleared string) there is no way to know. Of course you can just create 
    // a copy of the values, but that is not efficient in terms of memory.

    // string.clear(); //-> causes runtime error because empties the String, making it equal to ""

    // Slices take care of storing that information and also will not 
    // let the value getting invalidated
    let first_slice = &string[0..word];
    println!("first_slice = {}", first_slice);
    let second_slice = &string[word + 1..];
    println!("second_slice = {}", second_slice);

    let len = string.len();
    let full_string_slice = &string[0..len];
    println!("full_string_slice = {}", full_string_slice);
    
    let word_slice = first_word(&string);
    // string.clear(); //-> Rust does not let it happen due to muttable borrow -> WOW!
    println!("word_slice = {}", word_slice);

    // You can also have slices of arrays
    let a = [1, 2, 3, 4, 5];
    let slice = &a[1..3];
    assert_eq!(slice, &[2, 3]);
}


pub fn first_word_index(string: &String) -> usize {
    let bytes = string.as_bytes();

    for (i, &item) in bytes.iter().enumerate() { // Note thar .enumarate() returns a reference to the item
        if item == b' ' {
            return i;
        }
    }

    string.len()
}

// Slices of string literals are the same, so a better approach would be to 
// take a slice as a parameter to be more flexible
fn first_word(s: &String) -> &str {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return &s[0..i];
        }
    }

    &s[..]
}
