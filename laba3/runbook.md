# What is it

Тоже самое, как и во второй лабе, только к приложению добавляется логирование и визуализация, с использование Prometheus и Grafana. Все также у нас имеется мини flask приложение для проверки crud запросов с ипользованием базы данных с балансировкой трафика (nginx). Перед запуском приложения рекомендую ознакомится с заданием task.md

## Prestart

Поговорим, что находится в compose, в compose разворачивается наше приложение с nginx и Postgres, про это более подробно было расписано и показано в laba2, помимо этого у нас лежит 4 сервиса логирования, а именно grafana(визуализация), loki (хранилище логов), promtail (служба для сбора логов) и prometheus (prometei, для сбора и хранения метрик). И на последок есть два exporter, для базы и для nginx, поскольку данные компоненты не могут отдавать логи, придумана определенная сущность, как exporter

Мы ненмого разобрались, что лежит в compose можно приступать к запуску.

## Start


Чтобы запустить приложение для начала необходимо создать .env файл и прописать туда переменные, которые указаны в .env.example

Далее запусть compose.yaml, при помощи утилиты task:

```bash
task up

#Или если нет утилиты task, то ввести команду в терминале:
docker compose up --build -d
```

## Check Services

У нас поднялись все сервисы.

```bash
#flask, main app
localhost:8000 #ничего не будет, так как нет ui
localhost:8000/metrics #ручка с метриками

#grafana
localhost:3000 # us: admin pass: admin123

#promatail
localhost:9080

#prometheus 
localhost:9090

#loki 
localhost:3100  #ничего не будет, так как дб

# nginx_exporter
localhost:9113/metrics #метрики nginx

# postgres_exporter
localhost:9187/metrics #метрики postgres
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
## Monitoring

После проверки приложения, можно проверить наши метрики, если вы запускаете приложение первый раз, то вам будет необходимо экспортировать dashboards для postgres, flask и nginx, их можно экспортировать из каталога ./grafana/

Импортировать их нужно в grafana, после того, как они были импортированы, если вы не накосячили, то у вас покажутся красивые метрики приложения, если будут проблемы, то смотрите на datasorces, в которых может не быть Prometheus и loki, также гляньте в prometheus target health, все ли сервисы у вас подняты:

```bash
http://localhost:9090/targets
```

С приложением можно провести нагрузочное тестирование при помощи утилиты ab, где можно указать сколько запросов будут отправляться на опредленную ручку, и далее перейдя в dashboard можно заметить изменения на графиках.

```bash
# тема для тестирования 
ab -n 500 -c 50 http://localhost/users

ab -k -c 5 -n 20000 'http://localhost:8000/' & \
ab -k -c 5 -n 2000 'http://localhost:8000/test/400' & \
ab -k -c 5 -n 3000 'http://localhost:8000/test/409' & \
ab -k -c 5 -n 5000 'http://localhost:8000/test/500' & \
ab -k -c 50 -n 5000 'http://localhost:8000/test/200?seconds_sleep=1' & \
ab -k -c 50 -n 2000 'http://localhost:8000/test/200?seconds_sleep=2'

```