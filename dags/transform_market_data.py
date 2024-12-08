from pyspark.sql.types import FloatType, DoubleType

from transformed_data import MarketData
from pyspark.sql import functions as F


def transform_market_data(dfs: {}) -> {}:
    candle_df = dfs["candle"].withColumnRenamed("open", "open_cost")
    candle_df = candle_df.withColumnRenamed("close", "close_cost")
    candle_df = candle_df.withColumnRenamed("type_id", "type")
    candle_df = candle_df.withColumn("time", F.col("time").cast("timestamp"))

    candle_df = candle_df.withColumn("open_cost",
                              F.trim(F.regexp_replace(candle_df["open_cost"], ',', '.')).cast(DoubleType()))

    candle_df = candle_df.withColumn("close_cost",
                              F.trim(F.regexp_replace(candle_df["close_cost"], ',', '.')).cast(DoubleType()))

    dfs["candle"] = candle_df

    return MarketData(dfs["stock"], dfs["candle"])
