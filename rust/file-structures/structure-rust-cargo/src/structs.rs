use std::fmt;
struct AlwaysEqual;


struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}


impl User {
    fn print_login_message(&self) {
        println!("\nHello, {}!", self.username);
        // let len = self.username.len();
        // String::from("Hello, ") + &self.username[0..len] + &String::from("!")[0..len]
    }
}


// This can be replaced by using "println!("user = {:?}", user);"
impl fmt::Display for User {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "[\n   \"username\": \"{}\",\n   \"email\": \"{}\",\n   \"active\": \"{}\",\n   \"sign-in count\": \"{}\"\n]",
            self.username,
            self.email,
            self.active,
            self.sign_in_count
        )
    }
}


fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username: username,
        email: email,
        sign_in_count: 1,
    }
}


pub fn run_struct_demo() {
    let mut user = User {
        active: true,
        username: String::from("user"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };
    println!("\nuser = {}\n", user);

    // You can create a builder
    let _user1 = build_user(String::from("someone@example.com"), String::from("user1"));

    // Mutate values
    user.email = String::from("anotheremail@example.com");

    // Add methods
    user.print_login_message();

    // Assing None type values
    let _none_equivalent_struct = AlwaysEqual; // Equivalent to none
}
