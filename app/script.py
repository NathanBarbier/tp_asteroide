# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max
import math
from datetime import datetime

def update_asteroids(a,b):
    spark = SparkSession.builder.appName("MyApp").getOrCreate()

    old_df = None
    new_df = None

    try:
        new_df = spark.read.json("hdfs://namenode:9000/Data/asteroid_data/*.json")
    except Exception as e:
        print(e)

    try:
        old_df = spark.read.json("hdfs://namenode:9000/Data/updated_asteroid_data/*.json")
    except Exception as e:
        print(e)

    if old_df is not None and new_df is not None:
        df = new_df.union(old_df)
    elif old_df is not None and new_df is None:
        df = old_df
    elif old_df is None and new_df is not None:
        df = new_df
    else:
        return

    latest_updates = df.groupBy("asteroid_id").agg(spark_max("updated_at").alias("updated_at"))

    df = df.join(latest_updates, ["asteroid_id", "updated_at"])


    def update_position(asteroid_row):
        asteroid = asteroid_row.asDict()

        direction_magnitude = math.sqrt(
            asteroid["direction"]["x"] ** 2 + 
            asteroid["direction"]["y"] ** 2 + 
            asteroid["direction"]["z"] ** 2
        )

        normalized_direction = {
            "x": asteroid["direction"]["x"] / direction_magnitude,
            "y": asteroid["direction"]["y"] / direction_magnitude,
            "z": asteroid["direction"]["z"] / direction_magnitude
        }

        new_position = {
            "x": asteroid["position"]["x"] + normalized_direction["x"] * asteroid["velocity"],
            "y": asteroid["position"]["y"] + normalized_direction["y"] * asteroid["velocity"],
            "z": asteroid["position"]["z"] + normalized_direction["z"] * asteroid["velocity"]
        }

        return {
            "asteroid_id": asteroid["asteroid_id"],
            "size": asteroid["size"],
            "velocity": asteroid["velocity"],
            "direction": asteroid["direction"],
            "position": new_position,
            "updated_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    updated_asteroids = df.rdd.map(lambda row: update_position(row)).collect()

    updated_df = spark.createDataFrame(updated_asteroids)

    updated_df.show(truncate=False)

    df_to_send = df.selectExpr("CAST(asteroid_id AS STRING)", "to_json(struct(*)) AS value")

    df_to_send.write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("topic", "topic3") \
        .save()
    
    updated_df.write.mode("overwrite").json("hdfs://namenode:9000/Data/updated_asteroid_data/")