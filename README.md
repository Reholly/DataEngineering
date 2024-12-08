# DataEngineering
Исследовательский проект в университете

Поднятие проекта:
1) Поднимаем через docker-compose проект
2) Создаем БД airflow в поднятной постгре
3) Заходим в airflow-webserver и выполняем
```commandline
docker exec -it air-web /bin/bash

airflow users create     --username reholly     --password admin     --firstname admin     --lastname admin     --role Admin     --email eu.ustiantsev@yandex.ru

```
3) Запускаем через команду
```commandline
spark-submit --conf spark.driver.host=127.0.0.1  --jars spark/jars/postgresql-42.7.4.jar src/main.py --driver-memory 4g --executor-memory 4g
```
4) Наслаждаемся результатом