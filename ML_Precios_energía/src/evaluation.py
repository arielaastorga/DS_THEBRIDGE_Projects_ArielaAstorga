import pickle
from pathlib import Path
import pandas as pd

base_dir = Path(__file__).resolve().parent
ruta_modelo = base_dir.parent / "models" / "final_model.pkl"

with open(ruta_modelo, "rb") as f:
    final_model = pickle.load(f)


X_nuevo = pd.DataFrame([{
    'Month': 1,
    'Day': 1,
    'Temperature': 16.60,
    'Hour': 2,
    'Aerosol Optical Depth': 0.08,
    'Dew Point': 9.70,
    'DHI': 0,
    'DNI': 0,
    'GHI': 0,
    'Relative Humidity': 63.85,
    'Solar Zenith Angle': 134.40,
    'Pressure': 879,
    'Precipitable Water': 1.50,
    'Wind Direction': 353
}])

precio = final_model.predict(X_nuevo)

print('precio USD/MWh', precio)