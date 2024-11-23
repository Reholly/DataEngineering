from transformed_data import MarketData

def transform_market_data(dfs: {}) -> {}:
    candle_df = dfs["candle"].withColumnRenamed("open", "open_cost")
    candle_df = candle_df.withColumnRenamed("close", "close_cost")
    candle_df = candle_df.withColumnRenamed("type_id", "type")
    dfs["candle"] = candle_df

    return MarketData(dfs["stock"], dfs["candle"])
