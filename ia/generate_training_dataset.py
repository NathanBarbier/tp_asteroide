import numpy as np
import pandas as pd
import random
from IPython.display import display
import numpy as np
import pandas as pd

# Generate random asteroid
id = 0

def generate_asteroid():
    global id
    asteroid_data = {
        "asteroid_id": id,
        "mass": round(random.uniform(1e10, 1e18), 2),
        "size": round(random.uniform(10.0, 1000.0), 2),  
        "velocity": round(random.uniform(5.0, 50.0), 2), 
        "direction_x": round(random.uniform(0.0, 1000000.0), 2),
        "direction_y": round(random.uniform(0.0, 1000000.0), 2),
        "direction_z": round(random.uniform(0.0, 1000000.0), 2), 
        "position_x": round(random.uniform(0.0, 1000000.0), 2),
        "position_y": round(random.uniform(0.0, 1000000.0), 2),
        "position_z": round(random.uniform(0.0, 1000000.0), 2),
    }
    id += 1
    return asteroid_data

def generate_asteroid_dataframe(asteroid):    
    return pd.DataFrame([{
                        "asteroid_id": asteroid["asteroid_id"], 
                        "mass": asteroid["mass"],
                        "size": asteroid["size"], 
                        "velocity": asteroid["velocity"], 
                        "direction_x": asteroid["direction_x"],
                        "direction_y": asteroid["direction_y"],
                        "direction_z": asteroid["direction_z"],
                        "position_x": asteroid["position_x"],
                        "position_y": asteroid["position_y"],
                        "position_z": asteroid["position_z"]
                    }])


def generate_asteroids_dataframe(asteroids_to_generate_counter=10):
    # Génère 1000 astéroides
    asteroids = []
    for i in range(0, asteroids_to_generate_counter, 1):
        # Génération d'un asteroid
        asteroid = generate_asteroid()
        asteroids.append(asteroid)


    # Générer le dataframe contenant tous les astéroides
    asteroids_df = None
    for asteroid in asteroids:
        asteroid_df = generate_asteroid_dataframe(asteroid)
        
        if (asteroids_df is None):
            asteroids_df = asteroid_df;
        else:
            asteroids_df = pd.concat([asteroids_df, asteroid_df])

    return asteroids_df


df = generate_asteroids_dataframe(10)
df.reset_index(drop=True, inplace=True)
display(df)

def compute_gravitational_forces_between_two_objects(object_1, object_2):
    # constante gravitationelle
    G = 6.67430e-11

    # print(object_1, object_2)
    
    distance_x = object_1["position_x"] - object_2["position_x"]
    distance_y = object_1["position_y"] - object_2["position_y"]
    distance_z = object_1["position_z"] - object_2["position_z"]
    
    mass = object_1["mass"]
    size = object_1["size"]

    distance = np.sqrt(distance_x**2 + distance_y**2 + distance_z**2)
    
    attraction = G * (mass * size) / (distance**2 + 1)  # Ajout du +1 pour éviter la division par 0
    
    attraction_x = attraction * distance_x / distance
    attraction_y = attraction * distance_y / distance
    attraction_z = attraction * distance_z / distance

    return (float(attraction_x), float(attraction_y), float(attraction_z))


def compute_gravitational_forces(df):
    for asteroid in df.iterrows():

        attraction_x = 0
        attraction_y = 0
        attraction_z = 0

    for i, asteroid in df.iterrows():
        attraction_x = 0
        attraction_y = 0
        attraction_z = 0
        
        for j, other_asteroid in df.iterrows():
                if i != j:
                    attractions = compute_gravitational_forces_between_two_objects(asteroid, other_asteroid)
                    print(attractions)
                    
                    attraction_x += attractions[0]
                    attraction_y += attractions[1]
                    attraction_z += attractions[2]
        
        df.at[i, "attraction_x"] = attraction_x
        df.at[i, "attraction_y"] = attraction_y
        df.at[i, "attraction_z"] = attraction_z

        df.at[i, "direction_x"] += attraction_x
        df.at[i, "direction_y"] += attraction_y
        df.at[i, "direction_z"] += attraction_z

    return df


df = compute_gravitational_forces(df)

display(df)

df.to_csv("asteroids.csv", encoding='utf-8', index=False)
