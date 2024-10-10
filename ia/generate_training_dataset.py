import numpy as np
import pandas as pd
import random
from IPython.display import display

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


df = generate_asteroids_dataframe(2000)
df.reset_index(drop=True, inplace=True)
display(df)

import numpy as np
import pandas as pd

# def compute_gravitational_forces(df):
#     # Constante gravitationnelle
#     G = 6.67430e-11

#     df['attraction_x'] = 0.0
#     df['attraction_y'] = 0.0
#     df['attraction_z'] = 0.0

#     positions = df[['position_x', 'position_y', 'position_z']].values
#     masses = df['mass'].values

#     n = df.shape[0]
#     for i in range(n):
#         diffs = (positions[i] - positions[i+1:]) * 1000
#         distances = np.linalg.norm(diffs, axis=1)
#         masses_product = masses[i] * masses[i+1:]

#         attractions = G * masses_product / (distances**2 + 1)

#         forces = (attractions[:, np.newaxis] * diffs) / distances[:, np.newaxis]

#         df.loc[i, 'attraction_x'] += np.sum(forces[:, 0])
#         df.loc[i, 'attraction_y'] += np.sum(forces[:, 1])
#         df.loc[i, 'attraction_z'] += np.sum(forces[:, 2])

#         df.loc[i+1:, 'attraction_x'] -= forces[:, 0]
#         df.loc[i+1:, 'attraction_y'] -= forces[:, 1]
#         df.loc[i+1:, 'attraction_z'] -= forces[:, 2]

#     return df

# df = compute_gravitational_forces(df)

def compute_gravitational_forces_between_two_objects(object_1, object_2):
    G = 6.67430e-11
    
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

    return (attraction_x, attraction_y, attraction_z)


display(df)

df.to_csv("asteroids.csv", encoding='utf-8', index=False)





 
tools.display_dataframe_to_user(name="Attraction Dataset (Gravitational Logic)", dataframe=df)