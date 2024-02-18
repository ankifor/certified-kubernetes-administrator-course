

# Other
```bash
find ./folder-name -type f | xargs tail -n +1

ps -aux | grep kubelet

grep -A 2 -B 2 -i image
grep -nr namespace .

... | wc -l #count lines
cat -n 

echo -n "paswrd"| base64
echo -n "bX1zcWw=" | base64 --decode
```
# GREP and AWK

```bash
PODNAME=$(k get -n default pods | grep myapp | awk '{print $1}' | head -n1)

PODNAME=$(k get pods -o jsonpath="{.items[0].metadata.name}")



# surronding 10 lines
grep -C 10 "..."


awk '/ERROR/ {match($0, /ERROR/); print substr($0, RSTART - 500, RLENGTH + 5500);}' 2023-12-15.log
awk '/cert/ {match($0, /Cert/); print substr($0, RSTART - 100, RLENGTH + 300);}' x.log

awk '/POST/ {match($0, /POST/); print substr($0, RSTART - 500, RLENGTH + 1000);}' 2023-12-15.log
awk '/GET/ {match($0, /GET/); print substr($0, RSTART - 100, RLENGTH + 1000);}' x.log
awk '/debug/ {match($0, /debug/); print substr($0, RSTART - 500, RLENGTH + 1000);}' x.log


grep -i -o -E ".{20}ERROR.{20}" 2023-12-15.log
grep -i -o -E ".{20}gespeichert.{20}" 2023-12-18.log

jq '.' x.log > y.log
jq ' map( select(.thread | test("Hikari") | not))' y.log > w.log
date -d"2023-12-18T13:23" +%s
```

# Openshift

```bash
oc get pods -o=name -n ubreg-dev | grep bzst
oc exec --stdin --tty $POD -- /bin/bash

oc config view | grep namespace
alias ocns-set='oc config set-context --current --namespace'
alias ocns-get='oc config view | grep namespace'


oc get secret cloudera-kafka-secret-keytab -o jsonpath='{.data.keytab}' | base64 --decode > keytab
oc get secret dguv-server-cert-secret -o jsonpath="{.data}" | jq -r '."keystore.p12"' | base64 -d > keystore.p12


oc cp dateneingang-datenempfang-dguv-deployment-64b775dc98-qvdzm:tmp/log/dateneingang-datenempfang-dguv/2023-12-18.log ./x.log
oc cp dateneingang-datenempfang-bzst-deployment-84858cbdb7-s9mqg:tmp/log/dateneingang-datenempfang-bzst/2023-12-20.log ./x.log
oc cp dateneingang-datenempfang-bzst-deployment-5f45967c8c-pd2ns:etc/ssl/certs/truststore.p12 ./x.p12
```

# CURL

```bash
curl --parallel --parallel-immediate --parallel-max 3 http://frontend-monorepo-benchmark.workload.stba-e2.stba.cloud.intranet.bund.de/login

seq 1 20000 | xargs -n 1 -P 20 curl -Z -so --parallel-immediate "http://frontend-monorepo-benchmark.workload.stba-e2.stba.cloud.intranet.bund.de/login"


curl -v --cacert cacerts.pem --cert-type P12 --cert widnr_dabas-technical-dev.p12:******** --noproxy "*" https://dateneingang-datenempfang-bzst-system-test.workload.stba-e2.stba.cloud.intranet.bund.de/api/datenempfang/bzst

```



# When no binaries on the machine
```bash
# print file
echo $(</var/lib/minikube/certs/etcd/ca.crt)

# no ls
cd /to/dir
echo *


# input from file to var:
NAMESPACE=$(cat /var/run/secrets/kubernetes.io/serviceaccount/namespace)
NAMESPACE=$(</var/run/secrets/kubernetes.io/serviceaccount/namespace)

```

# HEREDOC
https://linuxize.com/post/bash-heredoc/

```bash
cat << EOF
The current working directory is: $PWD
You are logged in as: $(whoami)
EOF
```

Using `<<-` removes all leading spaces and tabs from the input
```bash
if true; then
    cat <<- EOF
    Line with a leading tab.
    EOF
fi

```

Any delimiter may be used, not only `EOF`
```bash
cat <<- something
...
something
```

Adding quotes to the delimiter prevents env vars from expanding
```bash
cat <<- "EOF"
The current working directory is: $PWD
You are logged in as: $(whoami)
EOF
```

It workds with piping and redirection
```bash
cat <<'EOF' |  sed 's/l/e/g' > file.txt
Hello
World
EOF


ssh -T user@host.com << EOF
echo "The current local working directory is: $PWD"
echo "The current remote working directory is: \$PWD"
EOF

```

# Remove strange files
find . -maxdepth 1 -type f -name "*~*" | xargs rm

# Mass renaming

```bash
# type -d for directories
find . -maxdepth 1 -type f | sed -e 'p' -E -e "s/'//g" -E -e "s/[()]/_/g" -E -e "s/(,| |_|)+/_/g" -E -e "s/_*-_*/-/g" -E -e "s/_\././g" -E -e "s/\b_//g" | xargs -n2 -d '\n' bash -c 'test "$0" != "$1" && echo "$0" "-->" "$1"'


find . -maxdepth 1 -type f | sed -e 'p' -E -e "s/&/_and_/g" -E -e "s/['’·]//g" -E -e "s/[()]/_/g" -E -e "s/(,| |_)+/_/g" -E -e "s/_*-_*/-/g" -E -e "s/(\b_|_\b)//g" | xargs -n2 -d '\n' bash -c 'test "$0" != "$1" && echo "$0" "-->" "$1"'


find . -maxdepth 1 -type f | sed -e 'p' -E -e "s/&/_and_/g" -E -e "s/['’·]//g" -E -e "s/[()]/_/g" -E -e "s/(,| |_)+/_/g" -E -e "s/_*-_*/-/g" -E -e "s/(\b_|_\b)//g" | xargs -n2 -d '\n' bash -c 'test "$0" != "$1" && mv "$0" "$1"'
```


# Rclone


```bash
/usr/bin/rclone sync ./Введение_в_сети_ЭВМ onedrive:/Documents/07_OtherStudies/Введение_в_сети_ЭВМ


```