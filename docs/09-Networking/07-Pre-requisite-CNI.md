# Pre-requisite CNI

  - Take me to [Lecture](https://kodekloud.com/topic/prerequsite-cni/)

In this section, we will take a look at **Pre-requisite Container Network Interface(CNI)**


![net-7](../../images/net7.PNG)

## Third Party Network Plugin Providers

- [Weave](https://www.weave.works/docs/net/latest/kubernetes/kube-addon/#-installation)
- [Calico](https://docs.projectcalico.org/getting-started/kubernetes/quickstart)
- [Flannel](https://github.com/coreos/flannel/blob/master/Documentation/kubernetes.md)
- [Cilium](https://github.com/cilium/cilium)


## To view the CNI Network Plugins

- CNI comes with the set of supported network plugins. 

```
$ ls /opt/cni/bin/
bridge  dhcp  flannel  host-device  host-local  ipvlan  loopback  macvlan  portmap  ptp  sample  tuning  vlan
```

## Docker 
- CNM - container network model
- does not support CNI
- kubernetes has a workaround for this
```bash
docker run --network=none nginx
bridge add 2e34dcf34 /var/run/netns/2e34dcf34
```



#### References Docs

- https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/


