# librerías de python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Modelos supervisados
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from xgboost import XGBRegressor

# Modelos no supervisados
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# Cross validation
from sklearn.model_selection import GridSearchCV

#Importo el mejor modelo
import pickle
import os


from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent
ruta_csv = base_dir.parent / "data" / "processed" / "meteo_processed.csv"

df = pd.read_csv(ruta_csv)

# el df con su X, y
X = df.drop(columns=['valor'])

# Valor es la variable target que es el precio de la electricidad
y = df['valor'].values

# Divido en train y en test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# MODELO SUPERVISADO
# Entreno con el mejor modelo XGBRegressor con MinMaxScaler()

pipe = Pipeline(steps=[
    ('scaler', MinMaxScaler()),
    ('regressor', XGBRegressor(
        random_state=42,
        n_jobs=-1,
        n_estimators=200,        
        max_depth=6,
        learning_rate=0.1        
    ))                           
])                               


# Entrenamiento
pipe.fit(X_train, y_train)

# Guardar el modelo en la carpeta models
# Ruta absoluta basada en la ubicación del script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')


# Guardar el modelo
with open(os.path.join(MODELS_DIR, 'final_model.pkl'), 'wb') as f:
    pickle.dump(pipe, f)

print('Entrenamiento supervisado OK')



# MODELO NO SUPERVISADO
# Esto es para analizar los grupos de precios de la electricidad 

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

k = 3
kmeans = KMeans(n_clusters=k, random_state=101, n_init=10)

# Entrenamiento
y_pred_km = kmeans.fit_predict(X_scaled)

print('Entrenamiento no supervisado OK')
