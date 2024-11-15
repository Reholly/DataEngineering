from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, MapType

class NewsDataTransformer:
    def transform(self, data: [], spark: SparkSession):
        data_df = spark.read.json(spark.sparkContext.parallelize([data]))
        # Создаем DataFrame для event
        event_df = data_df.select(
            F.col("uuid").alias("ID"),
            F.lit("Crime, Law and Justice").alias("main_theme"),  # Значение по умолчанию из categories
            F.col("title"),
            F.col("language"),
            F.col("published").alias("appearance_date"),
            F.col("url").alias("source_url")
        )

        # Создаем DataFrame для location
        location_schema = StructType([
            StructField("ID", StringType(), True),
            StructField("name", StringType(), True),
        ])

        location_df = data_df.select(
            F.lit("1").alias("ID"),  # Пример ID, можно сделать более динамично
            F.explode(data_df.entities.locations).name.alias("name")
        ).toDF("ID", "name")

        # Создаем DataFrame для event_per_location
        event_per_location_df = event_df.select(
            F.col("ID").alias("event_id"),
            F.lit("1").alias("location_id")  # Пример связанного id для location
        )

        # Создаем DataFrame для category
        category_df = spark.createDataFrame([
            ("1", "Crime, Law and Justice"),  # Пример ID, может быть динамическим
        ], ["ID", "name"])

        # Создаем DataFrame для event_per_category
        event_per_category_df = event_df.select(
            F.col("ID").alias("event_id"),
            F.lit("1").alias("category_id")  # Пример связанного id для category
        )

        return {
            "event": event_df,
            "location" : location_df,
            "category":category_df,
            "event_per_category" : event_per_category_df,
           "event_per_location" : event_per_location_df
        }