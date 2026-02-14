# Ansible. Example configs and best practises

## Мини инструкция по запуску playbook со своим python module.

Модуль написан на питоне, он принимает в качестве параметра порт для nginx и подставляет его в конфигурацию

## До запуска
Для теста вам нужно создать директорию для конфига nginx, можно использовать другой путь, но это самый простой вариант:
```bash
sudo mkdir -p /tmp/nginx-test        
# echo "server { listen 80; }" | sudo tee /tmp/nginx-test/nginx-web.conf
```
Сам файлик находитмся в /Task2/roles/module/file/nginx-web.conf, по дефолту в нем стоит 80 порт, поменяем мы потом его на 8080 при помощи питон скрипта

## Запуск

Чтобы запустить playbook вам нужно перейти в каталог roles/module и написать команду в терминале:

```bash
 ansible-playbook -i inventory.ini deploy.yaml 
```

Он применяет deploy файлик и invenoty.ini, который говорит нам о том что мы запускаемся с хоста.

Чтобы проверить, просто введите в терминале:
```bash 
 cat /tmp/nginx-test/nginx-web.conf
```
Там вы увидите, что поменялся порт с 80 на 8080.