from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, MapType
from pyspark.sql.functions import from_json, col
from script import update_asteroids

spark = SparkSession.builder.appName("AsteroidDataToCSV").getOrCreate()

spark.sparkContext.setLogLevel("WARN")

kafka_topic_name = "topic2"

kafka_bootstrap_servers = 'kafka:9092'

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .load()

df = df.selectExpr("CAST(value AS STRING)")

query = df.writeStream \
    .foreachBatch(update_asteroids) \
    .outputMode("update") \
    .start()

query.awaitTermination()

