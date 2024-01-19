
# Labeling convetions

https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
Example labels:

- release : stable / canary
- environment : dev /  qa / production
- tier : frontend / backend / cache
- partition : customerA / customerB
- track : daily / weekly

# Limitations
- 63 or less characters
- key-value pair
- name:
  - `([a-z0-9A-Z]+(-|_|\.)*)+`
  - prefix (optional): a DNS subdomain
  - <= 253 chars
  - `a.b.c/name`
  - if no prefix, name is assumed to be private to the user
  - `kubernetes.io/` and `k8s.io/` are reserved for core


# Selectors
Two types:
- equality-based 
- set-based

Multiple reqs via `,` = AND (`&&`)

## Equality based
Operators: 
- `=` / `==` (same meaning)
- `!=`

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: cuda-test
spec:
  containers:
    - name: cuda-test
      image: "registry.k8s.io/cuda-vector-add:v0.1"
      resources:
        limits:
          nvidia.com/gpu: 1
  nodeSelector:
    accelerator: nvidia-tesla-p100
```

## Set based
Operators: `in`, `notin`, `exists`

```
environment in (production, qa)
tier notin (frontend, backend)
partition
!partition
partition in (customerA, customerB),environment!=qa
```

## REST API
```
?labelSelector=environment%3Dproduction,tier%3Dfrontend
?labelSelector=environment+in+%28production%2Cqa%29%2Ctier+in+%28frontend%29
```

## Kubectl

```bash
k get pods -l environment=production,tier=frontend
k get pods -l 'environment in (production),tier in (frontend)'

# show listed labels
k get pods -Lapp -Ltier -Lrole

# update labels
k label pods -l app=nginx tier=fe
```

## Resources that support set-based requirements 
Supported by `Job`, `Deployment`, `ReplicaSet`, and `DaemonSet`

```yaml
selector:
  matchLabels:
    component: redis
  matchExpressions:
    - { key: tier, operator: In, values: [cache] }
    - key: tier
      operator: In
      values:
        - cache
    - { key: environment, operator: NotIn, values: [dev] }
```