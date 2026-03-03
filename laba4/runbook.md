## Тут пока просто солянка из того что я применял

Установка коллекции для применения манифестов куба
```bash
ansible-galaxy collection install kubernetes.core
pip install kubernetes openshift
```

## Смена пути конфига куба
```bash
ubuntu@lendy-2:~$ sudo mkdir -p /root/.kube
ubuntu@lendy-2:~$ sudo cp /home/ubuntu/.kube/config /root/.kube/config
ubuntu@lendy-2:~$ sudo chown root:root /root/.kube/config
ubuntu@lendy-2:~$ sudo chmod 600 /root/.kube/config
ubuntu@lendy-2:~$ sudo kubectl get nodes
```Ц

## Настройка доступа для удаленного доступа

Чтобы был доступ к вм необходимо настроить порт форвардинг при помощи команды
```bash
sudo kubectl port-forward --address 0.0.0.0 -n ingress-nginx service/ingress-nginx-controller 80:8080
```

Это не супер кайф способ, но тоже можно, чтобы постоянно не запускать port fowarding можно настроить nginx, который будет перенапрвлять трафик из minikube,
на самой ВМ для начала необходимо скачать nginx,
``` bash
sudo apt install nginx
```
И далее создать конфиг в который внести следующие параметры:
```bash
# создание конфига
sudo nano /etc/nginx/sites-enabled/kubernetes.conf

# что в него положить
server {
    listen 80;
    server_name myapp.local; # Сюда можно добавить и другие домены через пробел

    location / {
        proxy_pass http://192.168.49.2;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# после удалить default conf
sudo rm /etc/nginx/sites-enabled/default
```
## Отключение https у argocd
```bash
ubuntu@lendy-2:~$ kubectl patch cm argocd-cmd-params-cm -n argocd --type merge -p '{"data":{"server.insecure":"true"}}'
configmap/argocd-cmd-params-cm patched
ubuntu@lendy-2:~$ kubectl rollout restart deployment/argocd-server -n argocd
deployment.apps/argocd-server restarted
ubuntu@lendy-2:~$ kubectl rollout status deployment/argocd-server -n argocd
Waiting for deployment "argocd-server" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "argocd-server" rollout to finish: 1 old replicas are pending termination...
deployment "argocd-server" successfully rolled out
```

Он автоматически перенаправляет на защищенное подключение, но так как у нас нет tls сертификатов лучше офнуть это, добавив параметр в configMap

Получение пароля:
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}' | base64 -d
WxWL7tugIvCI-TUx #password
```