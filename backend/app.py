from flask import Flask, request, jsonify
from kafka import KafkaProducer
from marshmallow import Schema, fields, ValidationError
import json
import random

app = Flask(__name__)

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

class AsteroidSchema(Schema):
    count = fields.Int(required=True)

asteroid_schema = AsteroidSchema()

id = 0

def generate_asteroid():
    global id
    asteroid_data = {
        "asteroid_id": id,
        "size": round(random.uniform(10.0, 1000.0), 2),  
        "velocity": round(random.uniform(5.0, 50.0), 2), 
        "direction": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},  
        "position": {"x": round(random.uniform(0.0, 1000000.0), 2), "y": round(random.uniform(0.0, 1000000.0), 2), "z": round(random.uniform(0.0, 1000000.0), 2)},
    }
    id += 1
    return asteroid_data

@app.route('/asteroid', methods=['POST'])
def add_user():
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

    return jsonify({"message": "Asteroid data received and sent to Kafka"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5550)
