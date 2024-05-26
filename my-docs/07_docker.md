


```bash
docker run busybox echo "Hello World"


# to get the layers
docker history kubia:latest



# run an image
# 1234 is like a clusterip
docker run --name kubia-container -p 1234:8080 -d kubia



# list all running containers
docker ps


# like kubectl describe
docker inspect gcr.io/k8s-minikube/kicbase:v0.0.42 # image
docker inspect minikube # container

# logs of the containers (see docker ps)
docker logs 24e65f76e602
docker logs minikube 



$ docker stop kubia-container
$ docker rm kubia-container
$ docker rmi kubia:latest
```