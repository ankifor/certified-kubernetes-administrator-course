# ToDos

1) affinity 
2) taints drain
3) upgrade cluster
4) etcd
5) 





- try exam https://killer.sh/

- kubeadm
- etcdctl

- kube from scratch https://github.com/kelseyhightower/Kubernetes-the-hard-way
- Installation via kubeadm --> try with kodecloud
  - esp. CNI
  - new nodes
  - upgrade version
- backup / restore ETCD
- try `tr` command
- get familiar with search on kubernetes website
  - installation of kubeadm and cluster
- rollouts on deployment (strategies?)
- Create [Certs Overview](./24-k8s-crts-overview.md)

- Scheduling https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/

- train yq (merging)
- CoreDNS

- nsenter
- seccomp

 - storage
   - retain
   - same pv, multiple pvc


kubectl config view &
kill -STOP $!


Practice, Practice and Practice again. Do this until you can repeat things in your head without looking at your notes / documentation. This is especially true for ETCD Backup and Restore, Kubeadm Install and Upgrade. Even when fully memorised, practice again. Trust me, you do not want to rely on the docs to so heavily in the exam. 


- Kind (kubernetes in docker) as alternative to minikube
  - runs kubernetes in containers
  - controle plane is a container
  - worker nodes are also containers
  - https://kind.sigs.k8s.io/docs/user/quick-start/



- troubleshooting scheduler and worker nodes (`journalctl` and `systemctl`)

- Know how to define RBAC rules. 
  - Defining RBAC rules involves a couple of moving parts: the subject defined by users, groups, and ServiceAccounts; the RBAC-specific API resources on the namespace and cluster level; and, finally, the verbs that allow the corresponding operations on the Kubernetes objects. Practice the creation of subjects, and how to tie them together to form the desired access rules. Ensure that you verify the correct behavior with different constellations.
  



* EncryptionConfiguration
* Self-healing applications
    * Kubernetes provides additional support to check the health of applications running within PODs and take necessary actions through Liveness and Readiness Probes. However these are not required for the CKA exam and as such they are not covered here. These are topics for the Certified Kubernetes Application Developers (CKAD) exam and are covered in the CKAD course.
* Repeat Practice Backup and Restore
* https://minikube.sigs.k8s.io/docs/start/w 




- https://docs.linuxfoundation.org/tc-docs/certification/faq-cka-ckad-cks
- https://docs.linuxfoundation.org/tc-docs/certification/tips-cka-and-ckad#cka-and-ckad-environment 

- try tools `crictl`, `ctr`, `nerdcrt`