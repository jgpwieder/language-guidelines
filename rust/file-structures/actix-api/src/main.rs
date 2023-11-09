mod api;  // The compiler will look for the mod.rs file inside the api folder
use postgres::{Client, NoTls};
use postgres::Error as PostgresError;


use api::task::{
    get_task
};

use actix_web::{HttpServer, App, web::Data, middleware::Logger};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "debug");
    std::env::set_var("RUST_BACKTRACE", "1");
    env_logger::init();

    if let Err(e) = set_database() {
        println!("Error: {}", e);
        return Err(std::io::Error::new(std::io::ErrorKind::Other, "Database error"))
    }

    HttpServer::new(move || {
        let logger = Logger::default();
        App::new()
        .wrap(logger)
        .service(get_task)
    })
    .bind(("127.0.0.1", 80))?
    .run()
    .await
}

fn set_database() -> Result<(), PostgresError> {
    let mut client = Client::connect("postgresql://localhost:5432", NoTls)?;

    client.execute(
        "CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL
        )",
        &[]
    )?;

    Ok(())
}
