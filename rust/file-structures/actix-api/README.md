
# Cargo:

## Create cargo project:

cd to the desired directoty and run:
```sh
cargo new actix-api
```

## Build cargo project:

cd to the project's directoty and run:
```sh
cargo build
```

## Run executable:

cd to the project's directoty and run:
```sh
./target/debug/actix-api
```

## Run docker:

The binary actix-api is compiled with a version of the GNU C Library (GLIBC) that is not compatible with the version of GLIBC available in the base Debian Buster Slim image used. Therefore I needed to use a Debian Buster with Statically Linked Binary so that it includes all necessary libraries.

Must add the x86_64-unknown-linux-musl target using the rustup target add command.
```sh
rustup target add x86_64-unknown-linux-musl
```

Once the target is added, you can rebuild your Rust binary with the --target flag to specify the target architecture:
```sh
cargo build --release --target x86_64-unknown-linux-musl
```

Install musl cross:
```sh
brew install FiloSottile/musl-cross/musl-cross
```

Finally compose
```sh
 docker-compose up --build
```

# Postegris:

## Run Postgres docker:
```sh
docker run -p 5432:5432 -d \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=stripe-example \
    -v pgdata:/var/lib/postgresql/data \
    postgres
```

## Connect:
```sh
psql stripe-example -h localhost -U postgres
```

```sh
docker exec -it bdca2b8c09b7 psql -U postgres stripe-example
```
source: https://www.youtube.com/watch?v=G3gnMSyX-XM