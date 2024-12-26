# Alias and Completion
```bash
# if minikube https://minikube.sigs.k8s.io/docs/handbook/kubectl/
alias kubectl="minikube kubectl --" 


# https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#enable-shell-autocompletion
# system wide
k completion bash | sudo tee /etc/bash_completion.d/kubectl > /dev/null
# or for user (or append it to ~/.bashrc)
source <(kubectl completion bash)


alias k=kubectl
complete -o default -F __start_kubectl k



source <(kubectl completion bash | sed s/kubectl/k/g)
```


Get short names `k api-resources`