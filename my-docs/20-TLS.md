# TLS 
## Assurance of Private-Key Possession
Assurance of static (i.e., long-term) private-key possession shall be obtained before the use of the corresponding static public key. Assurance of public-key validity shall always be obtained prior to or concurrently with assurance of possession of the private key. Assurance of possession of the correct private key shall be obtained by the key-pair owner (e.g., ensuring that it is available and has not been modified before use). Entities that receive a public key shall obtain assurance that the key-pair owner possesses the private key corresponding to the received public key. 

For specific details regarding the assurance of the possession of private key-establishment keys, see SP 800-56A and SP 800-56B. For specific details regarding assurance of the possession of private digital-signature keys, see SP 800-89. Note that for public keys that are certified by a CA, the CA could obtain this assurance during the certification process. Otherwise, the owner and relying parties are responsible for obtaining the assurance.


https://tls12.xargs.org/

https://habr.com/ru/companies/ruvds/articles/696126/
