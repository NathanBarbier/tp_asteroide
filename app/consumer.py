from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType, MapType
from pyspark.sql.functions import from_json, col

# Créer la session Spark
spark = SparkSession.builder.appName("AsteroidDataToCSV").getOrCreate()

# Mute les logs inférieurs au niveau Warning
spark.sparkContext.setLogLevel("WARN")

# Sélectionner le topic
kafka_topic_name = "topic1"

# Sélectionner le serveur
kafka_bootstrap_servers = 'kafka:9092'

# Définir le schéma pour les données JSON
schema = StructType([
    StructField("asteroid_id", StringType(), True),
    StructField("size", FloatType(), True),
    StructField("velocity", FloatType(), True),
    StructField("direction", MapType(StringType(), FloatType()), True),
    StructField("position", MapType(StringType(), FloatType()), True),
    StructField("updated_at", StringType(), True)
])

# Récupération des données de mon stream kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic_name) \
    .load()

# Caster les données de mon string pour les rendre utilisables
df = df.selectExpr("CAST(value AS STRING)")

# Diviser les données JSON en colonnes avec le schéma défini
df = df.select(from_json("value", schema).alias("data")).select("data.*")

# Utiliser le partitionnement par asteroid_id pour créer un fichier par astéroïde
query = df \
    .writeStream \
    .format("json") \
    .option("path", "hdfs://namenode:9000/Data/asteroid_data") \
    .option("checkpointLocation", "hdfs://namenode:9000/Checkpoints/asteroid_checkpoint") \
    .outputMode("append") \
    .trigger(processingTime='1 seconds') \
    .start()
