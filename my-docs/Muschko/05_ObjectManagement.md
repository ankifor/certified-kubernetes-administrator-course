
# Introduction
- Declarative approach
- Imperative (through `kubectl`)

# Declarative approach

`kubectl apply -f ` works with files, directories (it may be a network location, incl. http), directory trees (flag `-R`)


# Kustomize
- https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- https://github.com/kubernetes-sigs/kustomize

- a tool in Kubernetes from 1.14
- Use cases:
  - generating manifests (e.g. generate a `ConfigMap` from a properties file)
  - Adding common configuration across multiple manifests. For example, adding a namespace and a set of labels for a Deployment and a Service.
  - Composing and customizing a collection of manifests. For example, setting resource boundaries for multiple Deployments.

- Execution modes
  - render processing output `kubectl kustomize <target>` (works like `--dry-run=client`)
  - create objects `kubectl apply -k <target>`

## Example 1

```yaml
.
├── config
│   ├── db-config.properties
│   └── db-secret.properties
├── kustomization.yaml
└── web-app-pod.yaml
```

```yaml
configMapGenerator:
- name: db-config
  files:
  - config/db-config.properties
secretGenerator:
- name: db-creds
  files:
  - config/db-secret.properties
resources:
- web-app-pod.yaml
```

Result: create `configmap`, `secret` and reference them in the `pod`.

## Example 2

```yaml
namespace: persistence
commonLabels:
  team: helix
resources:
- web-app-deployment.yaml
- web-app-service.yaml
```

Result: added label to the mentioned resources (also to `selector` / `matchLabels`)

## Example 3


```yaml
resources:
- nginx-deployment.yaml
patchesStrategicMerge:
- security-context.yaml
```

Patch file. At runtime, the patch strategy tries to find the container named nginx and enhances the additional configuration.
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  template:
  spec:
    containers:
    - name: nginx
      securityContext:
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
```

# yq
- https://github.com/mikefarah/yq (not the one from `apt`)
```bash
$ yq eval .metadata.name app-cache_deployment.yaml 
app-cache
$ yq eval .spec.template.spec.containers[0].image app-cache_deployment.yaml 
memcached:1.6.8
```
- modify inplace: 
```bash
$ yq e -i .spec.containers[0].env[1].value = "1.6.0" pod.yaml
```

- merge yamls:
```bash
$ cat sidecar.yaml
spec:
  containers:
  - image: envoyproxy/envoy:v1.19.1
    name: proxy-container
    ports:
    - containerPort: 80

$ yq eval-all 'select(fileIndex == 0) *+ select(fileIndex == 1)' pod.yaml sidecar.yaml
apiVersion: v1
kind: Pod
metadata:
  name: spring-boot-app
spec:
  containers:
  - image: bmuschko/spring-boot-app:1.5.3
    name: spring-boot-app
    env:
    - name: SPRING_PROFILES_ACTIVE
      value: prod
    - name: VERSION
      value: '1.5.3'
  - image: envoyproxy/envoy:v1.19.1
    name: proxy-container
    ports:
    - containerPort: 80
```


# Helm
- At runtime, it replaces placeholders in YAML template files with actual, end-user defined values.
- https://helm.sh/docs/
- https://artifacthub.io/packages/search?kind=0
  

## Standard Chart Structure
- Chart.yaml describes the meta information of the chart
  - https://helm.sh/docs/topics/charts/#the-chartyaml-file
  - must contain apiVersion, name, version
```yaml
apiVersion: 1.0.0
name: web-app
version: 2.5.4
```
- values.yaml contains the key-value pairs for substitution
```yaml
db_host: mysql-service
db_user: root
db_password: password
service_port: 3000
```

- tree structure
```bash
$ tree
.
├── Chart.yaml
├── templates
│   ├── web-app-pod-template.yaml
│   └── web-app-service-template.yaml
└── values.yaml
```

- templates are manifest files with placeholders
  - refer to values.yaml: `{{ .Values.<key> }}`
```yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    app: web-app
  name: web-app
spec:
  containers:
  - image: bmuschko/web-app:1.0.1
    name: web-app
    env:
    - name: DB_HOST
      value: {{ .Values.db_host }}
    - name: DB_USER
      value: {{ .Values.db_user }}
    - name: DB_PASSWORD
      value: {{ .Values.db_password }}
    ports:
    - containerPort: 3000
      protocol: TCP
  restartPolicy: Always
```


- commands
  - render current dir locally `helm template .`
  - package current dir `helm package .` (creates a `name-version.tgz` file)
