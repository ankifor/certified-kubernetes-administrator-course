

# Pod 

## Pod Problems / Flaws
- scalability
- failure tolerance

# ReplicaSet

Properties:
- controls replicas
- stable set of replicas
- rolling out a new version of pod
- purpose: availability
- Ownership
  - Links to pods via `metadata.ownerReferences` 
  - A ReplicaSet identifies new Pods to acquire by using its selector. If there is a Pod that has no OwnerReference or the OwnerReference is not a Controller and it matches a ReplicaSet's selector, it will be immediately acquired by said ReplicaSet
  - `.spec.template.metadata.labels` must match `spec.selector`, or it will be rejected by the API. 



# Deployment

Properties:
- incorporates a replicaset
- keeps version history and can rollback
- scaling of number of replicas
- same logic with labels as by ReplicaSet

```yaml
# kubectl create deployment app-cache --image=memcached:1.6.8 --replicas=4 --dry-run=client -o yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: app-cache
  name: app-cache
spec:
  replicas: 4
  selector:
    matchLabels:
      app: app-cache
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: app-cache
    spec:
      containers:
      - image: memcached:1.6.8
        name: memcached

```

## Use cases
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

- **Create a Deployment** to rollout a ReplicaSet. The ReplicaSet creates Pods in the background. Check the status of the rollout to see if it succeeds or not.
  - `kubectl rollout status deployment/nginx-deployment`
- **Declare the new state of the Pods** by updating the PodTemplateSpec of the Deployment. A new ReplicaSet is created and the Deployment manages moving the Pods from the old ReplicaSet to the new one at a controlled rate. Each new ReplicaSet updates the revision of the Deployment.
- **Rollback to an earlier Deployment revision** if the current state of the Deployment is not stable. Each rollback updates the revision of the Deployment.
- **Scale up the Deployment** to facilitate more load.
- **Pause the rollout** of a Deployment to apply multiple fixes to its PodTemplateSpec and then resume it to start a new rollout.
- **Use the status of the Deployment** as an indicator that a rollout has stuck.
- **Clean up older ReplicaSets** that you don't need anymore.



## Updating a deployment
Three ways:
- `set`: 
  - `kubectl set image deployment app-cache memcached=memcached:1.6.10 --record`
- `edit`:
- `apply`: edit the yaml definition and `k apply -f deploy.yaml` 

## Rollout History

```
$ kubectl rollout status deployment app-cache
Waiting for rollout to finish: 2 out of 4 new replicas have been updated...
deployment "app-cache" successfully rolled out

$ k rollout history deployment app-cache 
deployment.apps/app-cache 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

$ k rollout history deployment app-cache --revision 2
deployment.apps/app-cache with revision #2
Pod Template:
  Labels:	app=app-cache
	pod-template-hash=858b68bc5
  Containers:
   memcached:
    Image:	memcached:1.6.10
    Port:	<none>
    Host Port:	<none>
    Environment:	<none>
    Mounts:	<none>
  Volumes:	<none>

$ k rollout history deployment app-cache --revision 1
deployment.apps/app-cache with revision #1
Pod Template:
  Labels:	app=app-cache
	pod-template-hash=55d74ff68b
  Containers:
   memcached:
    Image:	memcached:1.6.8
    Port:	<none>
    Host Port:	<none>
    Environment:	<none>
    Mounts:	<none>
  Volumes:	<none>


```

## Rollback

```bash
$ kubectl rollout undo deployment app-cache --to-revision=1
deployment.apps/app-cache rolled back

# revision 1 turned into 3
$ k rollout history deployment app-cache 
deployment.apps/app-cache 
REVISION  CHANGE-CAUSE
2         <none>
3         <none>

```
