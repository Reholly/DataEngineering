from typing import List
from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from article_data_utils import Article
from transformed_data import NewsData


def transform_news(articles: List[Article], spark: SparkSession):
    event_df = spark.createDataFrame(
        [(article.uuid, article.title, article.url, article.published, article.language) for article in articles],
        schema=["uuid", "title", "source_url", "appearance_date", "language"])

    locations_data = [{"location": loc} for article in articles for loc in article.entities.locations]
    categories_data = [{"category": cat} for article in articles for cat in article.categories]

    locations_df = spark.createDataFrame(locations_data)
    categories_df = spark.createDataFrame(categories_data)

    unique_locations_df = locations_df.distinct().withColumn("id", F.monotonically_increasing_id())
    unique_categories_df = categories_df.distinct().withColumn("id", F.monotonically_increasing_id())

    # вспомогательный датафрейм для того чтобы объединить все это дело
    articles_df = spark.createDataFrame(
        [(article.uuid, article.title, article.entities.locations, article.categories) for article in articles],
        schema=["uuid", "title", "locations", "categories"])

    locations_link_df = articles_df.select("uuid", F.explode(articles_df.locations).alias("location")) \
        .join(unique_locations_df, "location") \
        .select("uuid", "id")

    categories_link_df = articles_df.select("uuid", F.explode(articles_df.categories).alias("category")) \
        .join(unique_categories_df, "category") \
        .select("uuid", "id")

    return NewsData(event_df, unique_locations_df, unique_categories_df, categories_link_df, locations_link_df)

