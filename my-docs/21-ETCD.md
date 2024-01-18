# ETCDCTL


## Install on a node
```bash
minikube ssh
sudo apt-get update -y
sudo apt-get install -y etcd-client
```
## Create my client-cert 
```bash

# ----------------
# do it wherever you need the cert
# it may also be the control plane node
# never transfer the key
# ----------------

openssl genrsa -out client-andrey.key 2048
openssl req -new -key client-andrey.key -subj "/CN=andrey/O=cka-study-guide" -out client-andrey.csr


minikube cp client-andrey.csr minikube:/home/andrey/client-andrey.csr

# ----------------
# minikube session
# ----------------
minikube ssh

sudo openssl x509 -req -in client-andrey.csr -CA /var/lib/minikube/certs/etcd/ca.crt -CAkey /var/lib/minikube/certs/etcd/ca.key -out client-andrey.crt -days 500


exit
# ----------------
# minikube session ended
# ----------------


minikube cp minikube:/home/docker/client-andrey.crt client-andrey.crt
```



## Get cert location und port
```bash
k -n kube-system describe po kube-apiserver-minikube | egrep etcd
  # --etcd-cafile=/var/lib/minikube/certs/etcd/ca.crt
  # --etcd-certfile=/var/lib/minikube/certs/apiserver-etcd-client.crt
  # --etcd-keyfile=/var/lib/minikube/certs/apiserver-etcd-client.key
  # --etcd-servers=https://127.0.0.1:2379


k -n kube-system describe po etcd-minikube | egrep client-url
# Annotations:          kubeadm.kubernetes.io/etcd.advertise-client-urls: # https://192.168.49.2:2379
#       --advertise-client-urls=https://192.168.49.2:2379
#       --listen-client-urls=https://127.0.0.1:2379,https://192.168.49.2:2379

k describe po etcd-minikube -n kube-system | egrep peer
# --peer-cert-file=/var/lib/minikube/certs/etcd/peer.crt
# --peer-client-cert-auth=true
# --peer-key-file=/var/lib/minikube/certs/etcd/peer.key
# --peer-trusted-ca-file=/var/lib/minikube/certs/etcd/ca.crt
```

## From kubectl
```bash
kubectl exec etcd-master -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /etc/kubernetes/pki/etcd/ca.crt --cert /etc/kubernetes/pki/etcd/server.crt  --key /etc/kubernetes/pki/etcd/server.key" 
```


## From control plane node
[`See client certs`](#create-my-client-cert) for the version with own  client certification.

```bash
minikube ssh


export ETCDCTL_API=3
export ETCDCTL_CACERT=/var/lib/minikube/certs/etcd/ca.crt
export ETCDCTL_CERT=/home/docker/certs/client-andrey.crt
export ETCDCTL_KEY=/home/docker/certs/client-andrey.key

etcdctl get /registry/ --prefix --keys-only --limit 10

# you can also these, but need the "sudo -E" for the command
export ETCDCTL_API=3
export ETCDCTL_CACERT=/var/lib/minikube/certs/etcd/ca.crt
export ETCDCTL_CERT=/var/lib/minikube/certs/apiserver-etcd-client.crt
export ETCDCTL_KEY=/var/lib/minikube/certs/apiserver-etcd-client.key



sudo -E etcdctl get /registry/ --prefix --keys-only --limit 10

```


## From etcd-minikube pod

```bash

# ssh or
k exec -it etcd-minikube -n kube-system -- sh 


export ETCDCTL_API=3
export ETCDCTL_CACERT=/var/lib/minikube/certs/etcd/ca.crt
export ETCDCTL_CERT=/var/lib/minikube/certs/etcd/peer.crt
export ETCDCTL_KEY=/var/lib/minikube/certs/etcd/peer.key


# sudo is needed because peer.key is protected

sudo -E etcdctl get /registry/ --prefix --keys-only --limit 10
sudo -E etcdctl endpoint health
sudo -E etcdctl snapshot save ~/etcd_backup.json -w json

# or use the full command
ETCDCTL_API=3 etcdctl --cacert ca.crt --cert peer.crt  --key peer.key --endpoints https://127.0.0.1:2379

```



## Commands
ETCDCTL_API=3


- `etcdctl get`
- `etcdctl put`
- `etcdctl endpoint health`

### Backup
```bash
$ etcdctl snapshot save /opt/etcd-backup-20240118.db
2024-01-18 01:34:17.654880 I | clientv3: opened snapshot stream; downloading
2024-01-18 01:34:17.668791 I | clientv3: completed snapshot read; closing
Snapshot saved at /opt/etcd-backup-20240118.db
```

### Restore

```bash
$ etcdctl snapshot restore /opt/etcd-backup-20240118.db --data-dir=/var/lib/from-backup

....

$ sudo ls /var/lib/from-backup
member


$ sudo /etc/kubernetes/manifests/etcd.yaml
...
spec:
volumes:
  ...
  - hostPath:
      path: /var/lib/from-backup
      type: DirectoryOrCreate
    name: etcd-data
  ...
```



# Installation of ETCD
## Automated Installatoin
just through `kubeadm`

`kubectl exec -it etcd-master -n kube-system -- etcdctl get / --prefix --keys-only`

## Manual Installation
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

