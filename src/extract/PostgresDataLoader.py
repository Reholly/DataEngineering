
from pyspark.sql import SparkSession, DataFrame


class PostgresDataLoader:
    def load_from_db(self, dsn: str, spark_session: SparkSession, properties) -> DataFrame:
        # Получаем список таблиц
        table_list = spark_session.read.jdbc(url=dsn, table="information_schema.tables", properties=properties) \
            .filter("table_schema = 'public'") \
            .select("table_name") \
            .collect()

        # Переменная для хранения объединенного DataFrame
        unified_df: DataFrame = None

        # Перебираем таблицы и загружаем данные
        for row in table_list:
            table_name = row.table_name
            print(f"Loading table: {table_name}")

            # Загружаем данные из таблицы
            df = spark_session.read.jdbc(url=dsn, table=table_name, properties=properties)

            # Если unified_df еще не инициализирован, присваиваем ему текущее значение df
            if unified_df is None:
                unified_df = df
            else:
                # Проверяем, совпадает ли структура таблиц перед объединением
                if unified_df.columns == df.columns:
                    unified_df = unified_df.union(df)
                else:
                    print(f"Skipping table {table_name} due to differing structure.")

        return unified_df