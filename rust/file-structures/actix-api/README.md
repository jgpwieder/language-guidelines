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


# Docker:

The binary actix-api is compiled with a version of the GNU C Library (GLIBC) that is not compatible with the version of GLIBC available in the base Debian Buster Slim image used. Therefore I needed to use a Debian Buster with Statically Linked Binary so that it includes all necessary libraries.

## Must add the x86_64-unknown-linux-musl target:
Using the rustup target add command.
```sh
rustup target add x86_64-unknown-linux-musl
```

## Install musl cross if not installed:
```sh
brew install FiloSottile/musl-cross/musl-cross
```

NOTE: May not be in PATH, if not:

1 Find it's path:
```sh
brew --prefix musl-cross
```

2 Edit path:
Add the /bin to the end of the output of previous command and add to your PATH
```sh
cd ~
nano .zshrc
```
ex: "/opt/homebrew/opt/musl-cross" + "/bin"

## Add configuration:
1 - crate ".cargo" directory inside the root project folder
2 - create "config" file with no extension 
3 - add the folllowing to the file:
```
[target.x86_64-unknown-linux-musl]
linker = "/opt/homebrew/opt/musl-cross/bin/x86_64-linux-musl-gcc"
```

x86_64-linux-musl-gcc
## Build your Rust binary with the --target flag:
NOTE: This is setup for a debian image, will not run in mac.

Once the target is added, you can rebuild your Rust binary with the --target flag to specify the target architecture:
```sh
cargo build --release --target x86_64-unknown-linux-musl
# for more info:
cargo build --release --target x86_64-unknown-linux-musl -v 
```

NOTE: Tou can speed it up using parallel compilation with the -j or --jobs flag with make (or gmake, which is the GNU Make command on some systems), you need to specify the number of CPU cores you want to use with the following:

```sh OPTIONAL
cargo build --release --target x86_64-unknown-linux-musl -jN
```
Replacing N with the desired number of cores.

## Finally compose
```sh
 docker-compose up --build
```

# Postegris:

## Run Postgres docker:
```sh
docker run -p 5432:5432 -d \
    -e POSTGRES_PASSWORD=joao \    
    -e POSTGRES_USER=joao \    
    -e POSTGRES_DB=joao-test \     
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