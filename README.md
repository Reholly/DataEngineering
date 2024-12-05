# DataEngineering
Исследовательский проект в университете

Поднятие проекта:
1) Поднимаем через docker-compose проект
2) Создаем БД airflow в поднятной постгре
3) Заходим в airflow-webserver и выполняем
```commandline
docker exec -it airflow-webserver /bin/bash

airflow users create     --username reholly     --password admin     --firstname admin     --lastname admin     --role Admin     --email eu.ustiantsev@yandex.ru

```
3) Запускаем через команду
```commandline
spark-submit --conf spark.driver.host=127.0.0.1  --jars spark/jars/postgresql-42.7.4.jar src/main.py --driver-memory 4g --executor-memory 4g
```
4) Наслаждаемся результатом


Рецепт шарлотки
Продукты (на 8 порций)	
Яблоки - 3 небольших (300 г)
Яйца C0 (крупные) - 4 шт.
Сахар - 200 г (можно 100-120 г)
Мука - 120 г (4-5 ст. ложек)
Сок лимона - 2 ст. ложки
Сахарная пудра (по желанию) - 0,5 ст. ложки
	
1
Подготовьте необходимые ингредиенты.
Яблоки желательно выбирать твёрдых сортов, кисло-сладкие. Я использовала красные яблоки и не очищала их, чтобы пирог выглядел красивее.
2
Яблоки нарежьте ломтиками 
3
Полейте нарезанные яблоки лимонным соком и перемешайте.
4
В большую миску разбейте яйца.
Включите духовку для разогрева до 180 градусов.
5
К яйцам всыпьте сахар. (Рекомендуют не сразу всыпать весь сахар, а добавлять частями при взбивании.)
В рецептах бисквитного теста количество сахара в столовых ложках часто соответствует количеству яиц. То есть для бисквита из 4-х яиц достаточно 4-5 ложек (и столько же ложек муки).
Но я добавила 1 стакан сахара (200 г) - бисквит получился сладким, но очень воздушным и пышным. Вы можете использовать меньше сахара (100-150 г), но учитывайте, что сахар влияет не только на сладость теста, но и на его структуру и плотность.

6
Миксером, на высокой скорости, взбивайте яйца с сахаром в течение 8-10 минут минимум. Масса должна стать светлой, пышной и увеличиться в несколько раз.
(Замечают, что на качество и скорость взбивания яиц может влиять форма венчиков миксера, и лучше всего - парные основные насадки).

7
В яичную смесь просейте частями муку через сито.

8
Лопаткой аккуратно вмешивайте муку снизу вверх, поднимающими движениями, чтобы тесто осталось воздушным, не осело.

9
Дно разъёмной формы для выпечки (диаметром 23-24 см) покройте пергаментом. Стенки формы смазывать маслом не нужно.
Если беспокоитесь, что пирог будет трудно вынуть из формы, смажьте ее маслом, но присыпьте при этом мукой, панировочными сухарями или манкой.

10
На дно формы выложите ломтики яблок.

11
Сверху яблоки залейте тестом.
(Можно выложить яблоки в два слоя, чередуя их с тестом.)

12
Выпекайте шарлотку в духовке, предварительно разогретой до 180 градусов, примерно 40 минут.
Важно духовку при выпечке бисквитного теста не открывать, по крайней мере первые 20 минут.

13
Готовую шарлотку остудите в форме.
Затем выложите бисквитный пирог с яблоками на блюдо, перевернув вверх дном, чтобы яблочные ломтики оказались сверху.

14
Когда яблочный пирог полностью остынет, можно посыпать его сахарной пудрой.

15
Приятного аппетита!


