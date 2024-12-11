from pyspark.sql import SparkSession, DataFrame


def load_market_data(dsn: str, spark_session: SparkSession, properties) -> dict[str, DataFrame]:
    table_list = spark_session.read.jdbc(url=dsn, table="information_schema.tables", properties=properties) \
        .filter("table_schema = 'public'") \
        .select("table_name") \
        .collect()

    dfs = {}

    print(table_list)
    for row in table_list:
        table_name = row.table_name
        print(f"Loading table: {table_name}")
        df = spark_session.read.jdbc(url=dsn, table=table_name, properties=properties)
        dfs[table_name]=df

    return dfs
