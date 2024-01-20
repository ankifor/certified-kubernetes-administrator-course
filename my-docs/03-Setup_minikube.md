# Minikube


## Windows
1. Activate Hyper-V
   1. Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
   2. https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v
2. Install Docker for Windows
   1. https://docs.docker.com/desktop/install/windows-install/
   2. no WSL2
   3. make sure Linux Containers are selected
3. Install minikube
4. https://minikube.sigs.k8s.io/docs/drivers/docker/
   1. minikube config set driver docker
5. Install openssh (actually, not needed)
   1. https://stackoverflow.com/questions/73603594/i-am-unable-to-start-openssh-with-windows-powershell
   2. https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell
   3. Get-WindowsCapability -Online -Name open* | Add-WindowsCapability -Online
   4. Get-WindowsCapability -Online -Name open*
   5. Start-Service sshd


## Linux


Install docker (https://docs.docker.com/engine/install/debian/)
```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update


usermod -aG docker $USER && newgrp docker

# see https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue/51362528#51362528
chmod 666 /var/run/docker.sock
```

Then install minikube (https://minikube.sigs.k8s.io/docs/start/)
```bash
cd ~/Downloads
su
wget https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
dpkg -i minikube_latest_amd64.deb

# normal user:
minikube config set driver docker
minikube start
```

# Metrics Server
https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/#before-you-begin

`minikube addons enable metrics-server`

`kubectl get apiservices | grep metrics` should return  `v1beta1.metrics.k8s.io`


`minikube dashboard` makes metrics available



Pods should contain resource requests:
```yaml
    resources:
      limits:
        cpu: 500m
        memory: 500Mi
      requests:
        cpu: 250m
        memory: 100Mi
```