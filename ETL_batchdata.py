# Databricks notebook source
storage_account_name = "https://iu-key.vault.azure.net/secrets/storageaccountname/9aa8fd5ef38b45aa8b84640ab656aad9"
storage_account_key = "https://iu-key.vault.azure.net/secrets/storageaccountkey/7cd28b56199e48a592ccf144f4990a67"
container = "iubhblobcontainer"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_key)

dbutils.fs.ls(f"wasbs://iubhblobcontainer@iubhblobdb.blob.core.windows.net/")

from pyspark.sql import SparkSession
from pyspark.sql.functions import col ,monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType


schema = StructType([
    StructField("Date", DateType(), True),
    StructField("Domain", StringType(), True),
    StructField("Location", StringType(), True),
    StructField("Value", IntegerType(), True),
    StructField("Transaction_count", IntegerType(), True)
])
df = spark.read \
  .option("header", "true") \
  .option("inferSchema", "true") \
  .option("delimiter", ",") \
  .csv(f"wasbs://iubhblobcontainer@iubhblobdb.blob.core.windows.net/bankdataset.csv")

df.show()



df.printSchema()



df.summary()

# Check for duplicate rows
duplicate_rows = df.groupBy(df.columns).count().where("count > 1")
if duplicate_rows.count() > 0:
    print("\nDuplicate rows found. Number of duplicate rows:", duplicate_rows.count())
else:
    print("\nNo duplicate rows found.")



df.filter("value is null").count()



df.distinct()



import psycopg2
from psycopg2.extras import execute_values
import pandas as pd

# Connect to PostgreSQL server
conn = psycopg2.connect(
    host="iudb.postgres.database.azure.com",
    database="iu_batchprocessed_db",
    user="https://iu-key.vault.azure.net/secrets/user/bf48e21ca07c4fdb9f4618d4302d3091",
    password="https://iu-key.vault.azure.net/secrets/password/46ea4f3fd80e4e92a4d1b83f4ceae15b3"
)


cursor = conn.cursor()


create_table_query = """
    CREATE TABLE IF NOT EXISTS iudeschema.bankdata (
        Id SERIAL PRIMARY KEY,
        Date DATE,
        Location VARCHAR(255),
        Value FLOAT,
        Transaction_count INT
    )
"""

create_index_query = """
    CREATE INDEX IF NOT EXISTS location_index 
    ON iudeschema.bankdata (Location)
"""

cursor.execute(create_table_query)
cursor.execute(create_index_query)

# Commit the changes and close the connection
conn.commit()
conn.close()




# Read CSV data from Azure Blob storage
df = spark.read.format("csv").option("header", "true").load("wasbs://iubhblobcontainer@iubhblobdb.blob.core.windows.net/bankdataset.csv")

# Add a column with unique IDs
df = df.withColumn("Id", monotonically_increasing_id())

# Write DataFrame to PostgreSQL table
df.write.format("jdbc") \
  .option("url", "jdbc:postgresql://iudb.postgres.database.azure.com:5432/iu_batchprocessed_db?currentSchema=iudeschema") \
  .option("dbtable", "bankdata") \
  .option("user", "https://iu-key.vault.azure.net/secrets/user/bf48e21ca07c4fdb9f4618d4302d3091") \
  .option("password", "https://iu-key.vault.azure.net/secrets/password/46ea4f3fd80e4e92a4d1b83f4ceae15b") \
  .mode("overwrite") \
  .save()
