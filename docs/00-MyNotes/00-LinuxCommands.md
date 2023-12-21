# Linux Commands

```bash
alias k=kubectl
find ./folder-name -type f | xargs tail -n +1

ps -aux | grep kubelet

grep -A 2 -B 2 -i image
grep -nr namespace .

... | wc -l #count lines
cat -n 

echo -n "paswrd"| base64
echo -n "bX1zcWw=" | base64 --decode
```


```bash
grep -o -E ".{200}gespeichert.{50}" 2023-11-28.log
grep -o -E ".{20}POST.{100}" 2023-11-28.log
grep -o -E ".{20}POST.{100}" 2023-12-01.log
grep -o -E ".{20}GET.{100}" 2023-12-01.log


awk '/ERROR/ {match($0, /ERROR/); print substr($0, RSTART - 500, RLENGTH + 5500);}' 2023-12-15.log
awk '/cert/ {match($0, /Cert/); print substr($0, RSTART - 100, RLENGTH + 300);}' x.log

awk '/POST/ {match($0, /POST/); print substr($0, RSTART - 500, RLENGTH + 1000);}' 2023-12-15.log
awk '/GET/ {match($0, /GET/); print substr($0, RSTART - 100, RLENGTH + 1000);}' x.log
awk '/debug/ {match($0, /debug/); print substr($0, RSTART - 500, RLENGTH + 1000);}' x.log


POST \"/api/datenempfang/dguv\

grep -i -o -E ".{20}ERROR.{20}" 2023-12-15.log
grep -i -o -E ".{20}gespeichert.{20}" 2023-12-18.log

jq '.' x.log > y.log
jq ' map( select(.thread | test("Hikari") | not))' y.log > w.log
date -d"2023-12-18T13:23" +%s



LOG.info("Entitaet Lieferdatei erfolgreich in DB gespeichert");


/api/datenempfang/dguv
/dateneingang/swagger-ui/index.html



oc get pods -o=name -n ubreg-dev | grep bzst
oc exec --stdin --tty -- /bin/bash

oc config view | grep namespace
alias ocns-set='oc config set-context --current --namespace'
alias ocns-get='oc config view | grep namespace'


oc get secret cloudera-kafka-secret-keytab -o jsonpath='{.data.keytab}' | base64 --decode > keytab
oc get secret dguv-server-cert-secret -o jsonpath="{.data}" | jq -r '."keystore.p12"' | base64 -d > keystore.p12


oc cp dateneingang-datenempfang-dguv-deployment-64b775dc98-qvdzm:tmp/log/dateneingang-datenempfang-dguv/2023-12-18.log ./x.log
oc cp dateneingang-datenempfang-bzst-deployment-84858cbdb7-s9mqg:tmp/log/dateneingang-datenempfang-bzst/2023-12-20.log ./x.log
oc cp dateneingang-datenempfang-bzst-deployment-5f45967c8c-pd2ns:etc/ssl/certs/truststore.p12 ./x.p12

------------------------
# certs

openssl req -in csr.csr -noout -text
openssl x509 -in certificate.crt -text -noout
openssl x509 -inform der -in CERTIFICATE.der -text -noout

openssl pkcs12 -in truststore_old.p12 -clcerts -nokeys -out publicCert.pem


certutil -encodehex keytab_nikiforov-a 1.txt 0x40000001
certutil -encode keytab_nikiforov-a 1.txt
certutil -decode 1.txt 3.txt
certutil -p pw -dump keystore.p12 > key.txt

openssl req -new -config ./openssl-server-certificates-etu.conf -key private-etu.key -out ubreg-etu-k8s-tls-csr.csr
openssl req -new -config ./openssl-server-certificates-vpu.conf -key private-vpu.key -out ubreg-vpu-k8s-tls-csr.csr
openssl req -new -config ./openssl-server-certificates-pru.conf -key private-pru.key -out ubreg-pru-k8s-tls-csr.csr


openssl pkcs12 -info -in x.p12 -passin pass:x | grep -E "(subject|issuer)"


openssl pkcs12 -export -nokeys -out truststore_new.p12 -in 0_tobi-sein-zertifikat.pem -in 0_widnr_dabas-technical-dev.pem -in rootca.pem


"C:\Program Files (x86)\Java\JRE\1.8.0_371\bin\keytool.exe" -import -file 0.pem -alias firstCA -keystore truststore_new.p12 -storetype PKCS12


#-------------------------
# curl

curl --parallel --parallel-immediate --parallel-max 3 http://frontend-monorepo-benchmark.workload.stba-e2.stba.cloud.intranet.bund.de/login
seq 1 20000 | xargs -n 1 -P 20 curl -Z -so --parallel-immediate "http://frontend-monorepo-benchmark.workload.stba-e2.stba.cloud.intranet.bund.de/login"


curl -v --cacert cacerts.pem --cert-type P12 --cert widnr_dabas-technical-dev.p12:******** --noproxy "*" https://dateneingang-datenempfang-bzst-system-test.workload.stba-e2.stba.cloud.intranet.bund.de/api/datenempfang/bzst



#-----------------------
# kafka


Kafka1-in.entw.rubd.stba.itzbund.net / 10.133.25.42
Kafka2-in.entw.rubd.stba.itzbund.net / 10.133.25.43
Kafka3-in.entw.rubd.stba.itzbund.net / 10.133.25.44



https://docs.confluent.io/cloud/current/access-management/authenticate/oauth/access-rest-apis.html

curl -X GET \
-H "Content-Type: application/vnd.kafka.binary.v2+json" \
-H "kafka.security.protocol: SASL_PLAINTEXT" \
-H "kafka.sasl.kerberos.service.name: kafka" \
-H "kafka.sasl.jaas.config: com.sun.security.auth.module.Krb5LoginModule required useTicketCache=true
serviceName=\"kafka\" useKeyTab=true keyTab=\"/home/user/keytab\"
principal=\"stba-rubd-etu_srv_caas_messaging@IAM.STBA\";" \
http://kafka1-in.entw.rubd.stba.itzbund.net/topics \
-w "%{http_code}"


curl -X POST \
-H "Content-Type: application/vnd.kafka.binary.v2+json" \
-H "kafka.security.protocol: SASL_PLAINTEXT" \
-H "kafka.sasl.kerberos.service.name: kafka" \
-H "kafka.sasl.jaas.config: com.sun.security.auth.module.Krb5LoginModule required useTicketCache=true
serviceName=\"kafka\" useKeyTab=true keyTab=\"/home/user/keytab\"
principal=\"stba-rubd-etu_srv_caas_messaging@IAM.STBA\";" \
http://kafka1-in.entw.rubd.stba.itzbund.net:9093/topics/caas_test \
--data '{"records":[{"key":"foo","value":"bar"}]}' \
-w "\n%{http_code}\n"
```
