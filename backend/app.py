import random
import time
import json

# Fonction pour générer des données d'astéroïdes simulées
def generate_asteroid_data():
    # Caractéristiques simulées de l'astéroïde
    asteroid_data = {
        "asteroid_id": random.randint(1000, 9999),
        "size": round(random.uniform(10.0, 1000.0), 2),  
        "velocity": round(random.uniform(5.0, 50.0), 2), 
        "distance_from_earth": round(random.uniform(0.1, 10.0), 4),  
        "orbital_period": round(random.uniform(0.5, 3.0), 2),  
        "direction_angle": round(random.uniform(0.0, 360.0), 2),  
    }
    return asteroid_data

# Fonction pour générer des données en continu
def simulate_asteroid_data_stream():
    while True:
        data = generate_asteroid_data()
        print(json.dumps(data))  # Print les données générées au format JSON
        time.sleep(1)  # Pause de 1 seconde entre chaque génération de données

# Exécuter la simulation
if __name__ == "__main__":
    simulate_asteroid_data_stream()
