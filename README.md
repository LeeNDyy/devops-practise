# Ansible. Example configs and best practises

## Мини инструкция по запуску playbook со своим python module.

Сам модуль написан на питоне, ансибл выводит из него message и changed. Очень простой нужен для теста.

## Запуск

Чтобы запустить playbook вам нужно перейти в каталог roles/module и написать команду в терминале:

```bash
 ansible-playbook -i inventory.ini deploy.yaml 
```

Он применяет deploy файлик и invenoty.ini, который говорит нам о том что мы запускаемся с хоста.
