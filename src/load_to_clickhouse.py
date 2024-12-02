from transformed_data import MarketData, NewsData
import clickhouse_connect


def load_to_clickhouse(result_df, news_data: NewsData, market_data: MarketData):
    client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='12345', database='market')

    for row in to_sql(news_data.Categories, "category"):
        print(row)
        client.command(row)

    for row in to_sql(news_data.Locations, "location"):
        print(row)
        client.command(row)

    for row in to_sql(news_data.Events, "event"):
        print(row)
        client.command(row)

    for row in to_sql(news_data.EventPerLocationLink, "categories_per_location"):
        print(row)
        client.command(row)

    for row in to_sql(news_data.EventPerCategoryLink, "categories_per_event"):
        print(row)
        client.command(row)

    for row in to_sql(result_df, "data_mart_fact"):
        print(row)
        client.command(row)

    for row in to_sql(market_data.Stocks, "stock"):
        print(row)
        client.command(row)

def to_sql(df, table_name):
    insert_queries = []

    for row in df.collect():
        values = []
        for col in df.columns:
            value = row[col]
            field_type = dict(df.dtypes)[col]

            if value is None:
                values.append("NULL")
            elif field_type == "timestamp":
                value = f"'{value}'"
                values.append(value)
            elif isinstance(value, str):
                value = f"'{value.replace("'", "")}'"
                values.append(value)
            else:
                values.append(str(value))

        values_str = ', '.join(values)
        insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({values_str});"
        insert_queries.append(insert_query)

    return insert_queries