
# API reference

https://kubernetes.io/docs/reference/using-api/api-concepts/

```
/api/v1/namespaces
/api/v1/pods
/api/v1/namespaces/rm/pods

/apis/apps/v1/namespaces/my-namespace/deployments
```




# Inspection of kubectl and certs
To get what kubectl is doing:
```bash
$ k get pods -n rm -v 6
I0119 14:10:02.733752  126787 loader.go:395] Config loaded from file:  /home/andrey/.kube/config
I0119 14:10:02.734702  126787 cert_rotation.go:137] Starting client certificate rotation controller
I0119 14:10:02.743345  126787 round_trippers.go:553] GET https://192.168.49.2:8443/api/v1/namespaces/rm/pods?limit=500 200 OK in 6 milliseconds
NAME         READY   STATUS    RESTARTS   AGE
disposable   1/1     Running   0          33m

``` 


in /home/andrey/.kube/config:
```
certificate-authority: /home/andrey/.minikube/ca.crt
...
client-certificate: /home/andrey/.minikube/profiles/minikube/client.crt
client-key: /home/andrey/.minikube/profiles/minikube/client.key
```

# Run curl with certs

```bash
# check config for certs:
k config view


curl --cacert ~/.minikube/ca.crt --cert ~/.minikube/profiles/minikube/client.crt --key ~/.minikube/profiles/minikube/client.key -X GET https://192.168.49.2:8443/api/v1/namespaces/rm/pods

```

# Run curl via proxy
kubectl proxy is a server that handles certificates for us, so that we don’t need to worry about auth tokens with curl.
```bash
$ k proxy &
Starting to serve on 127.0.0.1:8001
```

```bash
curl -X GET http://127.0.0.1:8001/api/v1/namespaces/rm/pods
```

# Run curl with a token
https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/#without-kubectl-proxy

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF
```

```bash
# wait for creation...
TOKEN=$(kubectl get secret default-token -o jsonpath='{.data.token}' | base64 --decode)
curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --cacert ~/.minikube/ca.crt
```



# From a pod
https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/


```bash
$ k get services -A
NAMESPACE     NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
default       kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP                  5d14h
kube-system   kube-dns     ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   5d14h
```

To find the location of a token, check pod specification:
```yaml
    volumeMounts:
    ...
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-lh2xx
      readOnly: true
```

```bash
$ ls /var/run/secrets/kubernetes.io/serviceaccount
ca.crt	namespace  token
```




```bash
# APISERVER=https://kubernetes.default.svc
APISERVER=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT_HTTPS
SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount
NAMESPACE=$(<${SERVICEACCOUNT}/namespace)
TOKEN=$(<${SERVICEACCOUNT}/token)
CACERT=${SERVICEACCOUNT}/ca.crt

$ curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api

# list pods in namespace rm
$ curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/namespaces/rm/pods

$ curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X GET ${APISERVER}/api/v1/namespaces/rm/pods/disposable
# delete rm/disposable

$ curl --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" -X POST ${APISERVER}/api/v1/namespaces/rm/pods/disposable?dryRun=client&delete=1

{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "pods \"disposable\" is forbidden: User \"system:serviceaccount:apps:api-access\" cannot create resource \"pods\" in API group \"\" in the namespace \"rm\"",
  "reason": "Forbidden",
  "details": {
    "name": "disposable",
    "kind": "pods"
  },
  "code": 403
}

```

# Selectors 

See [REST API in 23-Labels](./23-labels.md#rest-api)