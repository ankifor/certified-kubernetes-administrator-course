# ETCD

## Normal Kubernetes
```bash
kubectl exec etcd-master -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /etc/kubernetes/pki/etcd/ca.crt --cert /etc/kubernetes/pki/etcd/server.crt  --key /etc/kubernetes/pki/etcd/server.key" 
```

## Minikube

```bash

k -n kube-system describe po kube-apiserver-minikube | egrep etcd
  # --etcd-cafile=/var/lib/minikube/certs/etcd/ca.crt
  # --etcd-certfile=/var/lib/minikube/certs/apiserver-etcd-client.crt
  # --etcd-keyfile=/var/lib/minikube/certs/apiserver-etcd-client.key
  # --etcd-servers=https://127.0.0.1:2379


#############
minikube ssh
sudo apt-get update -y
sudo apt-get install -y etcd-client

cd /var/lib/minikube/certs/etcd/

sudo ETCDCTL_API=3 etcdctl --cacert ca.crt --cert server.crt --key server.key --endpoints https://127.0.0.1:2379 get /registry/ --prefix --keys-only --limit 10

sudo ETCDCTL_API=3 etcdctl --cacert ca.crt --cert peer.crt --key peer.key --endpoints https://127.0.0.1:2379 get /registry/ --prefix --keys-only --limit 10


# export ETCDCTL_API=3 

# for some reason, does not work with export of ETCDCTL_API
sudo ETCDCTL_API=3 etcdctl --cacert ca.crt --cert server.crt --key server.key --endpoints https://127.0.0.1:2379 get /registry/pods/kube-system/etcd-minikube 


sudo ETCDCTL_API=3 etcdctl --cacert ca.crt --cert server.crt --key server.key --endpoints https://127.0.0.1:2379 endpoint health

sudo ETCDCTL_API=3 etcdctl --cacert ca.crt --cert server.crt --key server.key --endpoints https://127.0.0.1:2379 snapshot save ~/etcd_backup.json -w json

```

Through etcd-minikube:

```bash
k describe po etcd-minikube -n kube-system | egrep peer

# --peer-cert-file=/var/lib/minikube/certs/etcd/peer.crt
# --peer-client-cert-auth=true
# --peer-key-file=/var/lib/minikube/certs/etcd/peer.key
# --peer-trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt


k exec -it etcd-minikube -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /var/lib/minikube/certs/etcd/ca.crt --cert /var/lib/minikube/certs/etcd/peer.crt  --key /var/lib/minikube/certs/etcd/peer.key" 

kubectl exec -it etcd-minikube -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /var/lib/minikube/certs/etcd/ca.crt --cert /var/lib/minikube/certs/etcd/peer.crt  --key /var/lib/minikube/certs/etcd/peer.key" 


# or connect to pod and execute
k exec -it etcd-minikube -n kube-system -- sh 

ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /var/lib/minikube/certs/etcd/ca.crt --cert /var/lib/minikube/certs/etcd/peer.crt  --key /var/lib/minikube/certs/etcd/peer.key
```







## Commands
ETCDCTL_API=3


- `etcdctl get`
- `etcdctl put`
- `etcdctl endpoint health`
- `etcdctl snapshot save`


## Installation
### Automated Installatoin
just through `kubeadm`

`kubectl exec -it etcd-master -n kube-system -- etcdctl get / --prefix --keys-only`

### Manual Installation
Download and install from github:
```bash
wget https://github.com/etcd-io/etcd/releases/download/v3.5.6/etcd-v3.5.6-linux-amd64.tar.gz

tar xvzf etcd-v3.5.6-linux-amd64.tar.gz

./etcd
```

You'll need to generate the keys and certificates (mtls).

```bash 
# etcd.service (Unit)
ExecStart=/usr/local/bin/etcd \\
--name ${ETCD_NAME} \\
--cert-file=/etc/etcd/kubernetes.pem \\
--key-file=/etc/etcd/kubernetes-key.pem \\
--peer-cert-file=/etc/etcd/kubernetes.pem \\
--peer-key-file=/etc/etcd/kubernetes-key.pem \\
--trusted-ca-file=/etc/etcd/ca.pem \\
--peer-trusted-ca-file=/etc/etcd/ca.pem \\
--peer-client-cert-auth \\ 
--client-cert-auth \\
--initial-advertise-peer-urls https://${INTERNAL_IP}:2380 \\
--listen-peer-urls https://${INTERNAL_IP}:2380 \\
--listen-client-urls https://${INTERNAL_IP}:2379, https://127.0.0.1:2379 \\
--advertise-client-urls https://${INTERNAL_IP}:2379 \\ 
--initial-cluster-token etcd-cluster-0 \\
--initial-cluster controller-0=https://${CONTROLLER0_IP}:2380, controller-1=https://${CONTROLLER1_IP}:2380 \\
--initial-cluster-state new \\
--data-dir=/var/lib/etcd
```

Option `--initial-cluster` with several controllers is needed for a HA setup.

