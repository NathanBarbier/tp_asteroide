from kafka import KafkaProducer
from time import sleep
import json
import random
import random
import time
import json


producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'topic1'

id = 0

def generate_data():
    asteroid_data = {
        "asteroid_id": id,
        "size": round(random.uniform(10.0, 1000.0), 2),  
        "velocity": round(random.uniform(5.0, 50.0), 2), 
        "direction_angle": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},  
        "pos": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},
    }
    id += 1
    return asteroid_data

try:
    while True:
        data = generate_data()
        producer.send(topic_name, value=data)
        print(f"Sent: {data}")
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping producer...")

producer.close()