# TLS 
## Assurance of Private-Key Possession
Assurance of static (i.e., long-term) private-key possession shall be obtained before the use of the corresponding static public key. Assurance of public-key validity shall always be obtained prior to or concurrently with assurance of possession of the private key. Assurance of possession of the correct private key shall be obtained by the key-pair owner (e.g., ensuring that it is available and has not been modified before use). Entities that receive a public key shall obtain assurance that the key-pair owner possesses the private key corresponding to the received public key. 

For specific details regarding the assurance of the possession of private key-establishment keys, see SP 800-56A and SP 800-56B. For specific details regarding assurance of the possession of private digital-signature keys, see SP 800-89. Note that for public keys that are certified by a CA, the CA could obtain this assurance during the certification process. Otherwise, the owner and relying parties are responsible for obtaining the assurance.


https://tls12.xargs.org/

https://habr.com/ru/companies/ruvds/articles/696126/



# RSA
```bash
openssl genrsa -out client-andrey.key 2048

# get modulus of the key
openssl rsa -in client-andrey.key -noout -modulus
openssl rsa -in client-andrey.key -noout -modulus | openssl md5

# get public key
openssl rsa -in client-andrey.key -pubout > client-andrey.pub
```


# CSR
```bash
openssl req -new -key client-andrey.key -subj "/CN=andrey/O=cka-study-guide" -out client-andrey.csr

# using a config
openssl req -new -config ./openssl-server-certificates-etu.conf -key private-etu.key -out ubreg-etu-k8s-tls-csr.csr


# get modulus of the csr
openssl req -in client-andrey.csr -noout -modulus

# get the description
openssl req -in client-andrey.csr -noout -text




```


# CRT
```bash
openssl x509 -req -in client-andrey.csr -CA /var/lib/minikube/certs/etcd/ca.crt -CAkey /var/lib/minikube/certs/etcd/ca.key -out client-andrey.crt -days 500

# or sign with a key for rootCA
openssl x509 -trustout -signkey ca.key -days 365 -req -in ca.csr -out ca.crt


# get the description
openssl x509 -in client-andrey.crt -noout -text

# get modulus of the crt (should have the same modulus as the private key)
openssl req -in client-andrey.crt -noout -modulus


# different format of the cert (binary DER)
openssl x509 -inform der -in CERTIFICATE.der -text -noout

# verify CA
openssl verify -CAfile /var/lib/minikube/certs/etcd/ca.crt client-andrey.crt

# verify for self-signed:
openssl verify -CAfile /var/lib/minikube/certs/etcd/ca.crt /var/lib/minikube/certs/etcd/ca.crt


# verify chain:
openssl verify -CAfile RootCert.pem -untrusted Intermediate.pem UserCert.pem


# get public key from crt
openssl x509 -in /var/lib/minikube/certs/etcd/ca.crt -noout -pubkey > ca.pub

# check signature #TBD
echo "hello world" > 1.txt
openssl pkeyutl -verify -in /var/lib/minikube/certs/etcd/ca.crt -inkey ca.pub -pubin




```

# PKCS12

```bash
# if password protected use flag
-passin pass:x 

# extract certs from p12
openssl pkcs12 -in truststore_old.p12 -clcerts -nokeys -out publicCert.pem


# extract key from p12
openssl pkcs12 -in truststore_old.p12 -clcerts -nocerts -out cert.key

# get infos from p12
openssl pkcs12 -info -in x.p12

# create p12
openssl pkcs12 -export -nokeys -out truststore_new.p12 -in 0_tobi-sein-zertifikat.pem -in 0_widnr_dabas-technical-dev.pem -in rootca.pem


# with password (keystore)
openssl pkcs12 -export -passout pass:x -out keystore.p12 -in server.cert -inkey server.key


```