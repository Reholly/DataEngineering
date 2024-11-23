# DataEngineering
Исследовательский проект в университете

Поднятие проекта:
1) Поднимаем через docker-compose проект
2) Запускаем через команду
```commandline
spark-submit --conf spark.driver.host=127.0.0.1  --jars spark/jars/postgresql-42.7.4.jar src/main.py --driver-memory 4g --executor-memory 4g
```
3) Наслаждаемся результатом