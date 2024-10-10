from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import r2_score

df = pd.read_csv("asteroids.csv")

X = df[['mass', 'size', 'velocity', 'direction_x', 'direction_y', 'direction_z', 'position_x', 'position_y', 'position_z']]
y_x = df['attraction_x']
y_y = df['attraction_y']
y_z = df['attraction_z']

X_train_x, X_test_x, y_train_x, y_test_x = train_test_split(X, y_x, test_size=0.8, shuffle=True)
X_train_y, X_test_y, y_train_y, y_test_y = train_test_split(X, y_y, test_size=0.8, shuffle=True)
X_train_z, X_test_z, y_train_z, y_test_z = train_test_split(X, y_z, test_size=0.8, shuffle=True)

model_x = LinearRegression()
model_y = LinearRegression()
model_z = LinearRegression()

model_x.fit(X_train_x, y_train_x)
model_y.fit(X_train_y, y_train_y)
model_z.fit(X_train_z, y_train_z)

y_pred_x = model_x.predict(X_test_x)
y_pred_y = model_y.predict(X_test_y)
y_pred_z = model_z.predict(X_test_z)

r2_x = r2_score(y_test_x, y_pred_x)
r2_y = r2_score(y_test_y, y_pred_y)
r2_z = r2_score(y_test_z, y_pred_z)

print("r2 x : ", r2_x)
print("r2 y : ", r2_y)
print("r2 z : ", r2_z)

mean_r2 = (r2_x + r2_y + r2_z) / 3

print("mean r2 : ", mean_r2)
if (mean_r2 > 0.80):
    print("Le modele est pas mal")
if (mean_r2 > 0.40 and mean_r2 < 0.60):
    print("Le modele ne sert à rien")
if (mean_r2 < 0.40):
    print("Le modele est à chier")
