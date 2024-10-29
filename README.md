# K1S
- https://hub.docker.com/_/httpd

# BUILD & RUN
```bash

# 빌드
$ docker build -t my-apache2 docker/httpd/

# 실행
$ docker run -dit --name my-running-app -p 8949:80 my-apache2

# 컨테이너 안으로
$ docker exec -it my-running-app bash
```

# LB
```
$ docker build -t blog docker/httpd
$ docker run -d --name blog-1 --rm blog
$ docker build -t lb docker/nginx
$ docker run -d --name ngix_lb -p 8949:80 --link blog-1 --rm lb
```

# COMPOSE
- https://docs.docker.com/reference/cli/docker/compose/up/
- https://docs.docker.com/compose/how-tos/file-watch/
```bash
$ docker compose -f docker-compose.yaml up -d 
$ docker compose up -d 
$ docker compose up -d --build
$ docker compose up -d --build --force-recreate
$ docker compose up -d --scale blog=1
$ docker compose up -d --scale blog=2
$ docker compose up -d --watch

$ docker compose stop
$ docker compose start
$ docker compose down
```

# COMPOSE scale IN/OUT
```
$ docker compose up -d \
> --scale blog=5 \
> --build
```
