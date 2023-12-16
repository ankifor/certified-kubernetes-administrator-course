# Minikube

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
