# Network Policies
  - Take me to [Video Tutorials](https://kodekloud.com/topic/network-policies-3/)
  
#### Trafic flowing through a webserver serving frontend to users an app server serving backend API and a database server

  ![traffic](../../images/traffic.PNG)
  
- There are two types of traffic
  - Ingress
  - Egress
  
   ![ing1](../../images/ing1.PNG)
  
   ![ing2](../../images/ing2.PNG)
  
## Network Security

  ![nsec](../../images/nsec.PNG)
  
## Network Policy

  ![npol](../../images/npol.PNG)
  
  ![npol1](../../images/npol1.PNG)
  
## Network Policy Selectors
  
  ![npolsec](../../images/npolsec.PNG)
  
## Network Policy Rules

  ![npol2](../../images/npol2.PNG)
  
## Create network policy
 
- To create a network policy
  ```
  apiVersion: networking.k8s.io/v1
  kind: NetworkPolicy
  metadata:
   name: db-policy
  spec:
    podSelector:
      matchLabels:
        role: db
    policyTypes:
    - Ingress
    ingress:
    - from:
      - podSelector:
          matchLabels:
            role: api-pod
      ports:
      - protocol: TCP
        port: 3306
  ```
  
  ```
  $ kubectl create -f policy-definition.yaml
  ```
  
 ![npol3](../../images/npol3.PNG)
 
 ![npol4](../../images/npol4.PNG)
  
## Note
 
 ![note1](../../images/note1.PNG)
 
#### Additional lecture on [Developing Networking Policies](https://kodekloud.com/topic/developing-network-policies/)

#### K8s Reference Docs
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
- https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/
 
  
  
# Egress deny all
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
```
  
# Egress allow dns

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-dns-policy
  namespace: default
spec:
  egress:
  - to:
    - podSelector:
        matchLabels:
          k8s-app: kube-dns
      namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    ports:
    - port: 53
      protocol: TCP
    - port: 53
      protocol: UDP
  podSelector: {}
  policyTypes:
  - Egress
```