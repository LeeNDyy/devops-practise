
Установка коллекции для применения манифестов куба
```bash
ansible-galaxy collection install kubernetes.core

pip install kubernetes openshift
```

ubuntu@lendy-2:~$ sudo mkdir -p /root/.kube
ubuntu@lendy-2:~$ sudo cp /home/ubuntu/.kube/config /root/.kube/config
ubuntu@lendy-2:~$ sudo chown root:root /root/.kube/config
ubuntu@lendy-2:~$ sudo chmod 600 /root/.kube/config
ubuntu@lendy-2:~$ sudo kubectl get nodes
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   12h   v1.26.3
ubuntu@lendy-2:~$ 