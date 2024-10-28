# K1S
- https://hub.docker.com/_/httpd

# Build & Run
```bash
# 빌드
$ docker build -t my-apache2 docker/httpd
# 실행
$ docker run -dit --name my-running-app -p 8949:80 my-apache2
# 컨테이너 안으로 이동
$ docker exec -it my-running-app bash
``` 
