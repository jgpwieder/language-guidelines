

# Postgres:
```sh
docker run -p 5432:5432 -d --name joaodb -e POSTGRES_PASSWORD=joaodb -e POSTGRES_USER=joaodb -e POSTGRES_DB=joaodb postgres
```

For memory restrictions:
```sh
docker run -p 5432:5432 -d --name joaodb -e POSTGRES_PASSWORD=joaodb -e POSTGRES_USER=joaodb -e POSTGRES_DB=joaodb --cpus='0.75' --memory='1.5GB' postgres
```


# Application:
get postgres host, can use localhost locally but need to do this for docker:
```sh
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' joaodb
```

```sh
 docker build -t fast-api-test .  
```

```sh
 docker run -it -p 8000:8000 fast-api-test
```

To provide memory restrictions
```sh
docker run -it -p 8000:8000 --cpus='0.25' --memory='0.5GB' fast-api-test
```

# Monitoring:

Create a docker network
```sh
docker network create monitoring
```

Run prometheus container:
```sh
docker run -d --name prometheus -p 9090:9090 --network monitoring prom/prometheus
```

Run Grafana container
```sh
docker run -d --name grafana -p 3000:3000 --network monitoring grafana/grafana
```
