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

def compute_gravitational_forces(df):
    # Constante gravitationnelle
    G = 6.67430e-11

    # Initialisation des colonnes d'attraction
    df['attraction_x'] = 0.0
    df['attraction_y'] = 0.0
    df['attraction_z'] = 0.0

    # Extraction des positions et des tailles sous forme de tableaux NumPy
    positions = df[['position_x', 'position_y', 'position_z']].values
    masses = df['mass'].values

    # Pré-calcul des forces gravitationnelles pour chaque paire
    n = df.shape[0]
    for i in range(n):
        diffs = (positions[i] - positions[i+1:]) * 1000  # Calcul des différences de positions
        distances = np.linalg.norm(diffs, axis=1)  # Distance euclidienne entre chaque paire (i, j)
        masses_product = masses[i] * masses[i+1:]  # Produit des masses pour chaque paire

        # Calcul de la force gravitationnelle (évite division par zéro en ajoutant +1 à distance^2)
        attractions = G * masses_product / (distances**2 + 1)

        # Composantes de la force gravitationnelle
        forces = (attractions[:, np.newaxis] * diffs) / distances[:, np.newaxis]

        # Mise à jour des forces gravitationnelles
        df.loc[i, 'attraction_x'] += np.sum(forces[:, 0])
        df.loc[i, 'attraction_y'] += np.sum(forces[:, 1])
        df.loc[i, 'attraction_z'] += np.sum(forces[:, 2])

        # Mise à jour des forces opposées (Newton)
        df.loc[i+1:, 'attraction_x'] -= forces[:, 0]
        df.loc[i+1:, 'attraction_y'] -= forces[:, 1]
        df.loc[i+1:, 'attraction_z'] -= forces[:, 2]

    return df

df = compute_gravitational_forces(df)
display(df)

df.to_csv("asteroids.csv", encoding='utf-8', index=False)