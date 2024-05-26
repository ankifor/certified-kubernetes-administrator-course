
# Motivation vs VMs
- as services get smaller, individual VMs become too expensive


# Differences from VMs
- containers are more lightweight 
  - no additional os-processes are needed
  - no separate resource pool
  - no guest OSes
  - container is basically the isolated application process
- goal: one process per container to reduce the complexity
- ![Sys calls](../images/06_containers/image.png)
  - Note: some hypervisors require a host OS, the other not
- ![alt text](../images/06_containers/image-1.png)
- security risks of containers are higher since the kernel is shared
- also memory limitations are important
- Note: memory swapping is disabled in k8s!!!


# Docker
- it is a platform for packaging, distributing and running applications
- Image
  - app
  - libs
  - other files
- App does not have access to the host's fs (typically)
- The only thing to matter about the hosts linux distribution: the kernel version and the kernel modules it loads
  - if a needed kernel module is not in the host, app cannot run
  - hw architecture (arm/x86) is also fixed


# Layers
- Containers consist of reusable layers
- ![alt text](../images/06_containers/image-2.png)
- docker stores each layer only once
- Copy-on-Write (CoW) mechanism (also happens on deletion, chown etc.)
- write layers are individual per container 
  


# Open Container Initiative
- OCI
- OCI Image Format Specification
- OCI Runtime Specification
- Kubernetes supports container runtime implementation via Container Runtime Interface (CRI)

- CRI-O is a lightweight alternative to docker
  - rkt, runC, Kata Containers
- ![Runtimes](../images/06_containers/image-3.png)