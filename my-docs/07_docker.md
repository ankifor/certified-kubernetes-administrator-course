


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



# https://blog.px.dev/container-filesystems/
#get the target's file system on the host
docker container inspect mycontainer | jq '.[0].GraphDriver' 

# LowerDir: Includes the filesystems of all the layers inside the container except the last one
# UpperDir: The filesystem of the top-most layer of the container. This is also # where any run-time modifications are reflected.
# MergedDir: A combined view of all the layers of the filesystem.
# WorkDir: An internal working directory used to manage the filesystem.
ls /proc/pid/root 
cat /proc/pid/mountinfo

# logs of the containers (see docker ps)
docker logs 24e65f76e602
docker logs minikube 



$ docker stop kubia-container
$ docker rm kubia-container
$ docker rmi kubia:latest


# entering the container
$ docker exec -it kubia-container bash

# -m = mount ns
# -t PID = attach to the target pid
$ nsenter -m -t 3130 sh




# using resources
# use cpu 1 and 2
$ docker run --cpuset-cpus="1,2" ...
# use 0.5 cpu time
$ docker run --cpus="0.5" ...

$ docker run --memory="100m" ...



```