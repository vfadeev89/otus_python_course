# Простой конкурентный веб сервер
Решение домашнего задания №4.

Пример запуска:
  - `python httpd.py`
  - Параметры запуска:
      - `-h` для справки
      - `-i --host` хост, по-умолчанию 0.0.0.0
      - `-p --port` порт, по умолчанию 8080
      - `-w --workers` кол-во воркеров, по-умолчанию 10
      - `-r --root` DOCUMENT ROOT, по-умолчанию текущий каталог при запуске
      - `-l <путь для записи логов скрипта>`

Запуск тестов:
  - `python httptest.py -v`

Результаты нагрузочного тестирования:
`$ ab -n 50000 -c 100 -r http://127.0.0.1:8080/httptest
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Send request failed!
Completed 5000 requests
Completed 10000 requests
Completed 15000 requests
Completed 20000 requests
Completed 25000 requests
Completed 30000 requests
Completed 35000 requests
Completed 40000 requests
Completed 45000 requests
Completed 50000 requests
Finished 50000 requests


Server Software:        Otus
Server Hostname:        127.0.0.1
Server Port:            8080

Document Path:          /httptest
Document Length:        34 bytes

Concurrency Level:      100
Time taken for tests:   436.421 seconds
Complete requests:      50000
Failed requests:        8
   (Connect: 3, Receive: 4, Length: 1, Exceptions: 0)
Write errors:           1
Total transferred:      8998920 bytes
HTML transferred:       1699796 bytes
Requests per second:    114.57 [#/sec] (mean)
Time per request:       872.843 [ms] (mean)
Time per request:       8.728 [ms] (mean, across all concurrent requests)
Transfer rate:          20.14 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   3.2      0     203
Processing:     0  863 512.4    857   19406
Waiting:        0  862 512.2    856   19406
Total:          1  863 512.3    858   19406

Percentage of the requests served within a certain time (ms)
  50%    858
  66%   1011
  75%   1064
  80%   1098
  90%   1192
  95%   1299
  98%   1485
  99%   1648
 100%  19406 (longest request)
`
