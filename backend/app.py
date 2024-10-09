from kafka import KafkaProducer
from time import sleep
import json
import random
from datetime import datetime
import random
import time
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
id = 0

def generate_data():
    asteroid_data = {
        "asteroid_id": id,
        "size": round(random.uniform(10.0, 1000.0), 2),  
        "velocity": round(random.uniform(5.0, 50.0), 2), 
        "distance_from_earth": round(random.uniform(0.1, 10.0), 4),  
        "orbital_period": round(random.uniform(0.5, 3.0), 2),  
        "direction_angle": round(random.uniform(0.0, 360.0), 2),  
    }
    id += 1
    return asteroid_data

while True:
    data = generate_data()
    producer.send('data-stream', data)
    print(f"Sent data: {data}")
    sleep(2)


