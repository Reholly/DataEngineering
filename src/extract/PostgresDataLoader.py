
from pyspark.sql import SparkSession, DataFrame


class PostgresDataLoader:
    def load_from_db(self, dsn: str, spark_session: SparkSession, properties) -> {}:
        # Получаем список таблиц
        table_list = spark_session.read.jdbc(url=dsn, table="information_schema.tables", properties=properties) \
            .filter("table_schema = 'public'") \
            .select("table_name") \
            .collect()


        dfs = {}
        # Перебираем таблицы и загружаем данные
        print("Загружаю таблицы")
        print(table_list)
        for row in table_list:
            table_name = row.table_name
            print(f"Loading table: {table_name}")
            # Загружаем данные из таблицы
            df = spark_session.read.jdbc(url=dsn, table=table_name, properties=properties)
            dfs[table_name]=df


        return dfs