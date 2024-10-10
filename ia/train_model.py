# # import pandas as pd
# # from sklearn.model_selection import train_test_split
# # from sklearn.linear_model import LinearRegression 
# # from sklearn.metrics import r2_score
# # from sklearn.preprocessing import StandardScaler

# # # Load the dataset
# # df = pd.read_csv("asteroids.csv")
# # print(df)


# # # Creating new variables
# # x = df[["mass", "size", "velocity", "direction_x", "direction_y", "direction_z", "position_x", "position_y", "position_z"]]
# # y = df[["attraction_x", "attraction_y", "attraction_z"]]

# # scaler = StandardScaler()
# # x_scaled = scaler.fit_transform(x)

# # # Splitting the data into training and testing
# # x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle=True, train_size=0.8)

# # # Creating a new model and fitting it
# # multi_model = LinearRegression()
# # multi_model.fit(x_train, y_train)

# # # Prediction new values
# # predictions = multi_model.predict(x_test)
# # r2 = r2_score(y_test, predictions)
# # # rmse = mean_squared_error(y_test, predictions, squared=False)

# # print('The r2 is: ', r2)
# # # print('The rmse is: ', rmse)






# import pandas as pd
# import numpy as np
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from sklearn.preprocessing import StandardScaler

# # Constante gravitationnelle
# G = 6.67430e-11  # en m^3 kg^-1 s^-2

# # Fonction pour calculer la force gravitationnelle entre deux astéroïdes
# def calculate_gravitational_force(mass_i, mass_j, distance):
#     return G * (mass_i * mass_j) / (distance**2 + 1e-10)  # éviter division par zéro

# # Fonction pour préparer les données pour le modèle machine learning
# def prepare_data_for_model(df):
#     # Initialisation des listes pour les features et les targets
#     features = []
#     targets = []
    
#     # Convertir les colonnes nécessaires en tableaux numpy pour accélérer les calculs
#     positions = df[['position_x', 'position_y', 'position_z']].values
#     masses = df['mass'].values
#     n = df.shape[0]  # Nombre d'astéroïdes

#     for i in range(n):
#         for j in range(i + 1, n):
#             # Calcul de la différence de position et de la distance entre les astéroïdes i et j
#             delta_pos = positions[j] - positions[i]
#             distance = np.linalg.norm(delta_pos)
            
#             if distance > 0:
#                 # Calcul de la force gravitationnelle (c'est notre target)
#                 force = calculate_gravitational_force(masses[i], masses[j], distance)
                
#                 # Création des features pour le modèle
#                 features.append([
#                     masses[i], masses[j],  # Masse des deux astéroïdes
#                     positions[i][0], positions[i][1], positions[i][2],  # Position de l'astéroïde i
#                     positions[j][0], positions[j][1], positions[j][2],  # Position de l'astéroïde j
#                     delta_pos[0], delta_pos[1], delta_pos[2],  # Différence de position
#                     distance  # Distance entre les astéroïdes
#                 ])
                
#                 # La target est la force gravitationnelle entre les deux astéroïdes
#                 targets.append(force)
    
#     # Conversion en DataFrame et retour
#     feature_columns = ['mass_i', 'mass_j', 'pos_i_x', 'pos_i_y', 'pos_i_z', 
#                        'pos_j_x', 'pos_j_y', 'pos_j_z', 'delta_x', 'delta_y', 'delta_z', 'distance']
    
#     features_df = pd.DataFrame(features, columns=feature_columns)
#     targets_df = pd.DataFrame(targets, columns=['force'])
    
#     return features_df, targets_df

# # Chargement des données
# df = pd.read_csv("asteroids.csv")

# # Préparation des données pour l'entraînement du modèle
# X, y = prepare_data_for_model(df)

# # Standardisation des données (recommandé pour les modèles de régression)
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# # Séparation des données en ensemble d'entraînement et de test
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.8, random_state=42)

# # Création et entraînement du modèle
# model = LinearRegression()
# model.fit(X_train, y_train)

# # Prédictions
# y_pred = model.predict(X_test)

# # Évaluation du modèle
# r2 = r2_score(y_test, y_pred)
# print(f'R² score: {r2}')

# # Affichage des premières prédictions et des vraies valeurs pour comparaison
# comparison_df = pd.DataFrame({'True Force': y_test.values.flatten(), 'Predicted Force': y_pred.flatten()})
# print(comparison_df.head())
