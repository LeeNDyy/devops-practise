# Что это

Это мини flask приложение для проверки crud запросов с ипользованием базы данных с балансировкой трафика (nginx). Перед запуском приложения рекомендую ознакомится с заданием task.md

## Start

Чтобы запустить приложение для начала необходимо создать .env файл и прописать туда переменные, которые указаны в .env.example.
Далее запусть compose.yaml, при помощи утилиты task:

```bash
task up

#Или если нет утилиты task, то ввести команду в терминале:
docker compose up --build -d
```

Чтобы проверить работу приложения, необходимо ввести в терминале команду ниже, она покажет список пользователей и информацию про них, которая берется из базы данных, ее конфигруация находится в файле init.sql

Далее приведены команды, использования crud запросов

```bash
curl -s http://localhost/users\?limit\=5 | python3 -m json.tool # вывод 5 юзеров

curl -s http://localhost/users/1 | jq . # вывод одого юзера

curl -X POST -s http://localhost/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Иван","surname":"Иванов","age":25,"town":"Москва"}' | jq . # создание пользователя

curl -X PUT -s http://localhost/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Петр","surname":"Петров","age":30,"town":"СПб"}' | jq . # обновление пользователя

curl -X DELETE http://localhost/users/1 # удаление пользователя плюс проверка, что его нет curl -s http://localhost/users/1 
ы

```