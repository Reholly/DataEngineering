from pyspark.sql.connect.dataframe import DataFrame


class MarketData:
    Stocks: DataFrame
    Candles: DataFrame
    def __init__(self,
                 stocks_df: DataFrame,
                 candles_df: DataFrame):
        self.Stocks = stocks_df
        self.Candles = candles_df

class NewsData:
    Events: DataFrame
    Locations: DataFrame
    Categories: DataFrame
    EventPerCategoryLink: DataFrame
    EventPerLocationLink: DataFrame

    def __init__(self,
                 events_df: DataFrame,
                 locations_df: DataFrame,
                 categories_df: DataFrame,
                 event_category_link_df: DataFrame,
                 event_location_link_df):
        self.Events = events_df
        self.Locations = locations_df
        self.Categories = categories_df
        self.EventPerLocationLink = event_location_link_df
        self.EventPerCategoryLink = event_category_link_df
