
### Проверка репликации, на машине необходимо запусть deploy.yaml, посл того как все обработается и выволится окей, то перенесется реплика, которую нужно будет потом запустить от рута данной командой

```bash
sudo -u postgres /usr/lib/postgresql/16/bin/pg_ctl -D /pg_data/16 start -w
```

После того как реплика запустилась на mastere можно посмотреть на хосту второй машины параметры, которые мы указывали при нагрузочном тестировании.

```bash
sudo -u postgres psql -c 'SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn FROM pg_stat_replication;'
```

Будет что то типо такого:
```
  client_addr   |   state   |  sent_lsn  | write_lsn  | flush_lsn  | replay_lsn 

 89.169.166.234 | streaming | 0/46000060 | 0/46000060 | 0/46000060 | 0/46000060
 ```