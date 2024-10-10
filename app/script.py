# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max
import math
from datetime import datetime


spark = SparkSession.builder.appName("MyApp").getOrCreate()

new_df = spark.read.json("hdfs://namenode:9000/Data/asteroid_data/")
old_df = spark.read.json("hdfs://namenode:9000/Data/updated_asteroid_data/")

df = new_df.union(old_df)

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

updated_df.write.mode("overwrite").json("hdfs://namenode:9000/Data/updated_asteroid_data/")


# asteroid_data = {
#     "asteroid_id": id,
#     "size": round(random.uniform(10.0, 1000.0), 2),  
#     "velocity": round(random.uniform(5.0, 50.0), 2), 
#     "direction_angle": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},  
#     "pos": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},
# }