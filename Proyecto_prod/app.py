# Importamos joblib para poder cargar el archivo model.pkl
import joblib

# Importamos Flask para crear la API,
# jsonify para devolver respuestas en formato JSON,
# y request para leer datos que envía el usuario
from flask import Flask, jsonify, request
import pandas as pd

# Creamos la aplicación Flask
# __name__ le indica a Flask dónde está el archivo principal
app = Flask(__name__)

# Esto activa el modo debug, muestra errores más detallados cuando estoy programando
app.config["DEBUG"] = False

#app.config["DEBUG"] = True


# Cargamos el "modelo" al iniciar la aplicación
# Esto hace que el modelo se lea una sola vez al arrancar la API
# y no en cada petición
model = joblib.load("model/model.pkl")

# Variables de entrada del modelo
# Esto debo hacerlo porque el modelo fue entrenado con columnas one_hot encodder

tipos_columnas = [
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "availability_365",
    "neighbourhood_cleansed_Arapiles",
    "neighbourhood_cleansed_Argüelles",
    "neighbourhood_cleansed_Berruguete",
    "neighbourhood_cleansed_Castillejos",
    "neighbourhood_cleansed_Cortes",
    "neighbourhood_cleansed_Cuatro Caminos",
    "neighbourhood_cleansed_Embajadores",
    "neighbourhood_cleansed_Gaztambide",
    "neighbourhood_cleansed_Goya",
    "neighbourhood_cleansed_Guindalera",
    "neighbourhood_cleansed_Ibiza",
    "neighbourhood_cleansed_Justicia",
    "neighbourhood_cleansed_Numancia",
    "neighbourhood_cleansed_Other",
    "neighbourhood_cleansed_Pacífico",
    "neighbourhood_cleansed_Palacio",
    "neighbourhood_cleansed_Palos de Moguer",
    "neighbourhood_cleansed_Pueblo Nuevo",
    "neighbourhood_cleansed_Puerta del Angel",
    "neighbourhood_cleansed_Recoletos",
    "neighbourhood_cleansed_San Diego",
    "neighbourhood_cleansed_Sol",
    "neighbourhood_cleansed_Trafalgar",
    "neighbourhood_cleansed_Universidad",
    "neighbourhood_cleansed_Valdeacederas",
    "neighbourhood_cleansed_Ventas",
    "room_type_Entire home/apt",
    "room_type_Private room"
]

campos_numericos = [
    "accommodates",
    "bathrooms",
    "bedrooms",
    "beds",
    "minimum_nights",
    "number_of_reviews",
    "review_scores_rating",
    "availability_365"
]

barrios = [
    "Arapiles",
    "Argüelles",
    "Berruguete",
    "Castillejos",
    "Cortes",
    "Cuatro Caminos",
    "Embajadores",
    "Gaztambide",
    "Goya",
    "Guindalera",
    "Ibiza",
    "Justicia",
    "Numancia",
    "Other",
    "Pacífico",
    "Palacio",
    "Palos de Moguer",
    "Pueblo Nuevo",
    "Puerta del Angel",
    "Recoletos",
    "San Diego",
    "Sol",
    "Trafalgar",
    "Universidad",
    "Valdeacederas",
    "Ventas"
]

tipos_alquiler = [
    "Entire home/apt",
    "Private room"
]


# Ruta principal de la API
# Se ejecuta cuando alguien entra a la URL raíz "/"
# En la terminal bash:   http://localhost:5000/
# En render:  https://tu-api.onrender.com/

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API Flask para prediccion de apartamentos",
        "endpoints": ["/health", "/predict_query", "/predict"]
    })


# Para comprobar rápidamente si la API está funcionando
# Sólo significa que el proceso Flask está vivo y puede responder una petición HTTP en esa ruta
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "running"
    })


# Ruta con parámetro en el path, para recibir por ejemplo el nombre de un barrio
# Ejemplo: /neighbourhood/Sol
# El valor "Sol" se guarda en la variable name

# RUTA CON PARÁMETROS DE LA QUERY PARA USAR LA FUNCIÓN DE PREDICCIÓN
# Recibe los datos que necesita el modelo para hacer las predicciones

def preparar_fila_entrada(data):

    # Compruebo que estén los campos de neighbourhood_y room type, y sino manda un error

    missing = [campo for campo in campos_numericos + ["neighbourhood_cleansed", "room_type"] if campo not in data]

    if missing:
        raise ValueError(f"Faltan campos requeridos: {', '.join(missing)}")

    row = {}

    # Compruebo que estos campos sean numéricos
    for campo in campos_numericos:
        try:
            row[campo] = float(data[campo])
        except (TypeError, ValueError):
            raise ValueError(f"El campo '{campo}' debe ser numérico")

    # Los convierto en string y le quito los espacios
    neighbourhood = str(data["neighbourhood_cleansed"]).strip()

    room_type = str(data["room_type"]).strip()

    if neighbourhood not in barrios:
        raise ValueError(
            f"Barrio no válido. Usa uno de: {', '.join(barrios)}"
        )

    if room_type not in tipos_alquiler:
        raise ValueError(
            f"room_type no válido. Usa uno de: {', '.join(tipos_alquiler)}"
        )

    for col in tipos_columnas:
        if col not in row:
            row[col] = 0

    neighbourhood_col = f"neighbourhood_cleansed_{neighbourhood}"
    room_type_col = f"room_type_{room_type}"

    if neighbourhood_col in row:
        row[neighbourhood_col] = 1

    if room_type_col in row:
        row[room_type_col] = 1

    return pd.DataFrame([row], columns=tipos_columnas)



# PREDICCION DE RESULTADOS
# PREDICT QUERY
# /predict_query?neighbourhood=Sol&room_type=Entire%20home/apt&minimum_nights=5...
@app.route("/predict-query", methods=["GET"])
def predict_query():
    try:
        data = request.args.to_dict()
        X = preparar_fila_entrada(data)
        prediction = model.predict(X)[0]

        return jsonify({
            "prediccion_precio": round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


# PREDICT POST

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Debes enviar un JSON válido"}), 400

        X = preparar_fila_entrada(data)
        prediction = model.predict(X)[0]

        return jsonify({
            "predicccion_precio": round(float(prediction), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400



# Manejador de error 404
# Se activa cuando el usuario entra en una ruta que no existe
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Ruta no encontrada"
    }), 404


# Manejador de error 500
# Se activa cuando ocurre un error interno en el servidor
@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Error interno del servidor"
    }), 500

