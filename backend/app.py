from flask import Flask, request, jsonify
from flask_cors import CORS
from kafka import KafkaProducer, KafkaConsumer
from marshmallow import Schema, fields, ValidationError
import json
import random

app = Flask(__name__)
CORS(app)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
consumer = KafkaConsumer(
    'topic3', 
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest',  
    group_id='flask-group'
)
class AsteroidSchema(Schema):
    count = fields.Int(required=True)

asteroid_schema = AsteroidSchema()

id = 0

def generate_asteroid():
    global id
    condition = True
    while condition:
        asteroid_data = {
            "asteroid_id": id,
            "size": round(random.uniform(10.0, 1000.0), 2),  
            "velocity": round(random.uniform(5.0, 50.0), 2), 
            "direction": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},  
            "position": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},
        }
        if asteroid_data["position"]["x"] != 0 and asteroid_data["position"]["y"] != 0 and asteroid_data["position"]["z"] != 0:
            condition = False
    id += 1
    return asteroid_data

@app.route('/asteroid', methods=['POST'])
def add_asteroid():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = asteroid_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    asteroids = []
    for i in range(0, data['count'], 1):
        asteroids.append(generate_asteroid())

    
    producer.send('topic1', asteroids)
    producer.flush()
    return jsonify(asteroids, 200)

@app.route('/asteroid', methods=['GET'])
def get_asteroid():

    producer.send('topic2', "Hello, World!")
    producer.flush()

    response_message = None
    for message in consumer:
        response_message = message.value
        break  

    if response_message:
        return jsonify({"message": response_message}), 200
    else:
        return jsonify({"error": "No response received"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
