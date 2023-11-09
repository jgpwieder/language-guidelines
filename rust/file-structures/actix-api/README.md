
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

```sh
 docker-compose up --build
```


## Run postegris:
```sh
docker run -p 5432:5432 -d \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=stripe-example \
    -v pgdata:/var/lib/postgresql/data \
    postgres
```

```sh
# connect
psql stripe-example -h localhost -U postgres

docker exec -it bdca2b8c09b7 psql -U postgres stripe-example
```
source: https://www.youtube.com/watch?v=G3gnMSyX-XM