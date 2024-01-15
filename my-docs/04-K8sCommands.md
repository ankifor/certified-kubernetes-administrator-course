# Kubernetes Commands
- [Kubernetes Commands](#kubernetes-commands)
  - [Kubectl gets](#kubectl-gets)
  - [Other](#other)
  - [Certificates](#certificates)
  - [Connect to node](#connect-to-node)
  - [Kubelet](#kubelet)


## Namespace and Alias
```bash
kubectl config set-context <context-of-question> --namespace=<namespace-of-question>
kubectl config use-context <context-of-question>

alias k=kubectl


kubectl api-resources
```




## Kubectl gets
```bash
k get pods 
k describe pod myapp-pod

k get replicationcontroller
k get replicaset
k get replicaset new-rs -o yaml
k get deployment
k get daemonsets
k get serviceaccount 
k get clusterrolebinding
k get configmaps
k get secrets
k get all

k get pod --all-namespaces
k get pod -A

k get pod --namespace=dev
k get pod -n=dev
k get pod --watch #monitor changes
k get pod -o=wide
k get pods --selector app=App1
k get pods --show-labels
k get pod --selector env=dev
k get all --selector env=dev


# https://kubernetes.io/docs/reference/kubectl/jsonpath/
k get pods -o json
k get pods -o=jsonpath='{@}'
k get pods -o=jsonpath='{.items[0]}'
k get pods -o=jsonpath='{.items[0].metadata.name}'
k get pods -o=jsonpath="{.items[*]['metadata.name', 'status.capacity']}"
k get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.startTime}{"\n"}{end}'
k get pods -o=jsonpath='{.items[0].metadata.labels.kubernetes\.io/hostname}'
```

## Information

```
k explain pods.spec
```


## Resource deletion
```bash
# do not wait!!
k delete pod nginx --force 
```


## Other
```bash
k exec etcd-master -n kube-system etcdctl get / --prefix -key

k exec etcd-master -n kube-system -- sh -c "ETCDCTL_API=3 etcdctl get / --prefix --keys-only --limit=10 --cacert /etc/kubernetes/pki/etcd/ca.crt --cert /etc/kubernetes/pki/etcd/server.crt  --key /etc/kubernetes/pki/etcd/server.key" 



docker ps

k delete pod webapp
k run nginx --image nginx
k create -f pod.yaml
k replace -f pod.yaml
k replace --force -f pod.yaml #to delete and create if not directly replacable
k apply -f pod.yaml
k scale --replicas=6 replicaset myapp-replicaset
k edt replicaset new-rs
# create a yaml description of pod
k run redis --image redis --dry-run=client -o yaml



# create deployment
k create deployment --image=nginx --replicas=4 nginx --dry-run=client -o yaml

#create service
k expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml
k expose pod nginx --type=NodePort --port=80 --name=nginx-service --dry-run=client -o yaml

k create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml


# switch namespace
k config set-context $(k config current-context) --namespace=dev



k taint nodes node1 app=blue:NoSchedule
k describe node kubemaster | grep Taint

k label node node-1 size=Large
k get node --show-labels


k get events
k logs my-custom-scheduler -n kube-system



k top node
k top pod


k logs -f even-simulator-pod event-simulator
k logs -f even-simulator-pod

k rollout status deployment/myapp-deployment
k rollout history deployment/myapp-deployment
k rollout undo deployment/myapp-deployment



k create configmap app-config --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod
k create configmap app-config --from-file=app_config.properties



k create secret generic app-secret --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=paswrd




k drain node-1
k cordon node-1
k uncordon node-1


kubeadm upgrade plan

k config get-clusters
k config use-context cluster1


```

## Certificates
```bash
# generate Keys: 
openssl genrsa -out ca.key 2048
# generate CSR: 
openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" -out ca.csr
#Sign certificates: 
openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt
```
## Connect to node
```bash
k exec -it <pod> -- /bin/bash
###
k get node -o=wide
ssh <ip>
####
scp cluster1-controlplane:/opt/cluster1.db /opt/cluster1.db
```


## Kubelet

```bash


ps -aux | grep kubelet


cat /etc/kubernetes/manifests/kube-apiserver.yaml

# Non-kubeadm setup
cat /etc/systemd/system/kube-apiserver.service


cat /etc/systemd/system/kube-controller-manager.service
# kubeadm
cat /etc/kubernetes/manifests/kube-controller-manager.yaml


cat /etc/kubernetes/manifests/kube-scheduler.yaml


k -n elastic-stack exec -it app -- cat /log/app.log
k exec --stdin --tty shell-demo -- /bin/bash
```