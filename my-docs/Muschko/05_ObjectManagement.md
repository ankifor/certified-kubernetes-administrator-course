
# Introduction
- Declarative approach
- Imperative (through `kubectl`)

# Declarative approach

`kubectl apply -f ` works with files, directories (it may be a network location, incl. http), directory trees (flag `-R`)


# Kustomize
- https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/
- https://github.com/kubernetes-sigs/kustomize
- https://github.com/kubernetes-sigs/kustomize/tree/master/examples/transformerconfigs

- a tool in Kubernetes from 1.14
- Use cases:
  - generating manifests (e.g. generate a `ConfigMap` from a properties file). See [Example 1](./00-exercises/ex_chapter4/kust/example1/)
  - Adding common configuration across multiple manifests. For example, adding a namespace and a set of labels for a Deployment and a Service. See [Example 2](./00-exercises/ex_chapter4/kust/example2/)
  - Composing and customizing a collection of manifests. For example, setting resource boundaries for multiple Deployments. See [Example 3](./00-exercises/ex_chapter4/kust/example3/) and [Example 4](./00-exercises/ex_chapter4/kust/example4/)
  - [Example 5](./00-exercises/ex_chapter4/kust/example5/) Replacements of vars
  - [Example 6](./00-exercises/ex_chapter4/kust/example6/) Base and overlays

- Execution modes
  - render processing output `kubectl kustomize <target>` (works like `--dry-run=client`)
  - create objects `kubectl apply -k <target>`
  - view created objects: `kubectl get -k <target>`
  - also works with `describe`, `delete` and `diff`

- Feature list: https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/#kustomize-feature-list
  - namespace
  - commonLabels
  - commonAnnotations
  - bases
  - vars
  - images 
```yaml
images:
  - name: postgres
    newName: my-registry/my-postgres
    newTag: v1
  - name: nginx
    newTag: 1.8.0
  - name: my-demo-app
    newName: my-app
  - name: alpine
    digest: sha256:25a0d4
```
  - configurations: they may change behaviour of features (more here https://github.com/kubernetes-sigs/kustomize/tree/master/examples/transformerconfigs)
```yaml
#kustomization.yaml
namePrefix:
  alices-
nameSuffix:
  -v2
resources:
- resources.yaml
configurations:
- namePrefix-config.yaml
```

```yaml
#namePrefix-config.yaml
namePrefix:
- path: metadata/name
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
