from pyspark.sql import SparkSession

# Create Spark session
spark = SparkSession.builder \
    .appName("Connect to Postgres") \
    .getOrCreate()

# Define JDBC connection properties
url = "jdbc:postgresql://iudb.postgres.database.azure.com:5432/iu_batchprocessed_db?currentSchema=iudeschema"
properties = {
    "user": "https://iu-key.vault.azure.net/secrets/user/bf48e21ca07c4fdb9f4618d4302d3091",
    "password": "https://iu-key.vault.azure.net/secrets/password/46ea4f3fd80e4e92a4d1b83f4ceae15b",
    "driver": "org.postgresql.Driver"
}

# Load data from Postgres table
df = spark.read \
    .format("jdbc") \
    .option("url", url) \
    .option("dbtable", "bankdata") \
    .option("user", properties["user"]) \
    .option("password", properties["password"]) \
    .option("driver", properties["driver"]) \
    .load()

# Write the dataframe to Azure Blob Storage as a table in Parquet format
storage_account_name = "https://iu-key.vault.azure.net/secrets/storageaccountname/9aa8fd5ef38b45aa8b84640ab656aad9"
storage_account_key = "https://iu-key.vault.azure.net/secrets/storageaccountkey/7cd28b56199e48a592ccf144f4990a67"
container = "dtable"

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_key)
df.write.format("parquet").save(f"wasbs://iubhblobcontainer@iubhblobdb.blob.core.windows.net/dtable")

# # Stop SparkSession
spark.stop()