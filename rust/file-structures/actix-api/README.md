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
rustup target add x86_64-unknown-linux-gnu
```

## Install musl cross if not installed:
```sh
# Currently, there is no equivalent of musl-cross for GNU in Homebrew for macOS. Cross-compiling for GNU/Linux on macOS is non-trivial and typically involves using a Docker container with a GNU/Linux environment for compatibility.
```

NOTE: May not be in PATH, if not:

1 Find it's path:
```sh
brew --prefix gcc
```

2 Edit path:
Add the /bin to the end of the output of previous command and add to your PATH
```sh
cd ~
nano .zshrc
```

Add:
```sh
export PATH="/path/to/gcc/bin:$PATH"

```
ex: "/opt/homebrew/opt/musl-cross" + "/bin"

## Add configuration:
1 - crate ".cargo" directory inside the root project folder
2 - create "config" file with no extension 
3 - add the folllowing to the file:
```
[target.x86_64-unknown-linux-gnu]
linker = "gcc"  
# OR if the gcc you have is from homebrew, could be: 
linker = "/opt/homebrew/opt/gcc/bin/gcc"
# Go there snd try to find executable
```

x86_64-linux-musl-gcc
## Build your Rust binary with the --target flag:
NOTE: This is setup for a debian image, will not run in mac.

Once the target is added, you can rebuild your Rust binary with the --target flag to specify the target architecture:
```sh
cargo build --release --target x86_64-unknown-linux-gnu
# for more info:
cargo build --release --target x86_64-unknown-linux-gnu -v
```

## Finally compose
```sh
 docker-compose up --build
```


# Postegris:

## Run Postgres docker:
```sh
docker run -p 5432:5432 -d \
    -e POSTGRES_PASSWORD=joaodb \    
    -e POSTGRES_USER=joaodb \    
    -e POSTGRES_DB=joaodb \     
    -v pgdata:/var/lib/postgresql/data \
    postgres
```
```sh
docker run -p 5432:5432 -d --name joaodb -e POSTGRES_PASSWORD=joaodb -e POSTGRES_USER=joaodb -e POSTGRES_DB=joaodb postgres

```

## Connect:
```sh
docker ps
```

```sh
docker exec -it CONTAINER_ID psql -U postgres
```

List databases:
```sql
SELECT datname FROM pg_database;
```

```sql
CREATE USER mynewuser WITH PASSWORD 'newpassword';
ALTER ROLE mynewuser CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO mynewuser;
```
source: https://www.youtube.com/watch?v=G3gnMSyX-XM