from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, MapType, IntegerType
from pyspark.sql.functions import from_json, col, regexp_replace, explode,ArrayType

# Créer la session Spark
spark = SparkSession.builder.appName("AsteroidDataToCSV").getOrCreate()

# Mute les logs inférieurs au niveau Warning
spark.sparkContext.setLogLevel("WARN")

# Sélectionner le topic
kafka_topic_name = "topic1"

# Sélectionner le serveur
kafka_bootstrap_servers = 'kafka:9092'

# Définir le schéma pour les données JSON
schema = ArrayType(StructType([
    StructField("asteroid_id", IntegerType(), True),
    StructField("size", FloatType(), True),
    StructField("velocity", FloatType(), True),
    StructField("direction", StructType([
      StructField("x", FloatType(), True),
      StructField("y", FloatType(), True),
      StructField("z", FloatType(), True),
    ]), True),
    StructField("position", StructType([
      StructField("x", FloatType(), True),
      StructField("y", FloatType(), True),
      StructField("z", FloatType(), True),
    ]), True),
    StructField("updated_at", StringType(), True)
]))

# Récupération des données de mon stream kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .load()
    
df_string = df.selectExpr("CAST(value AS STRING)") 
df_json = df_string.select(from_json("value", schema).alias("data")).select(explode(col("data")).alias("asteroid")).select("asteroid.*")
df_json.writeStream \
    .format("console") \
    .option("truncate", "false") \
    .outputMode("append") \
    .start() 


query = df_json \
    .writeStream \
    .format("json") \
    .option("path", "hdfs://namenode:9000/Data/asteroid_data") \
    .option("checkpointLocation", "hdfs://namenode:9000/Checkpoints/asteroid_checkpoint") \
    .outputMode("append") \
    .trigger(processingTime='1 seconds') \
    .start() \
    .awaitTermination()
