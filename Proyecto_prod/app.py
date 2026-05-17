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

MODEL_COLUMNS = [
    "minimum_nights",
    "number_of_reviews",
    "availability_365",
    "neighbourhood_Acacias",
    "neighbourhood_Almagro",
    "neighbourhood_Almenara",
    "neighbourhood_Arapiles",
    "neighbourhood_Argüelles",
    "neighbourhood_Bellas Vistas",
    "neighbourhood_Berruguete",
    "neighbourhood_Castillejos",
    "neighbourhood_Cortes",
    "neighbourhood_Cuatro Caminos",
    "neighbourhood_Embajadores",
    "neighbourhood_Gaztambide",
    "neighbourhood_Goya",
    "neighbourhood_Guindalera",
    "neighbourhood_Ibiza",
    "neighbourhood_Justicia",
    "neighbourhood_Lista",
    "neighbourhood_Numancia",
    "neighbourhood_Other",
    "neighbourhood_Pacífico",
    "neighbourhood_Palacio",
    "neighbourhood_Palos de Moguer",
    "neighbourhood_Prosperidad",
    "neighbourhood_Pueblo Nuevo",
    "neighbourhood_Puerta del Angel",
    "neighbourhood_Recoletos",
    "neighbourhood_Rios Rosas",
    "neighbourhood_San Diego",
    "neighbourhood_San Isidro",
    "neighbourhood_Sol",
    "neighbourhood_Trafalgar",
    "neighbourhood_Universidad",
    "neighbourhood_Valdeacederas",
    "neighbourhood_Ventas",
    "room_type_Entire home/apt",
    "room_type_Private room"
]

VALID_NEIGHBOURHOODS = [
    "Acacias", "Almagro", "Almenara", "Arapiles", "Argüelles",
    "Bellas Vistas", "Berruguete", "Castillejos", "Cortes",
    "Cuatro Caminos", "Embajadores", "Gaztambide", "Goya",
    "Guindalera", "Ibiza", "Justicia", "Lista", "Numancia",
    "Other", "Pacífico", "Palacio", "Palos de Moguer",
    "Prosperidad", "Pueblo Nuevo", "Puerta del Angel",
    "Recoletos", "Rios Rosas", "San Diego", "San Isidro",
    "Sol", "Trafalgar", "Universidad", "Valdeacederas", "Ventas"
]

VALID_ROOM_TYPES = [
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

# @pie sintax
# Es un decorado de una función o un objeto, se utiliza para modificar su comportamiento
@app.route("/neighbourhood/<string:name>", methods=["GET"])
def get_neighbourhood(name):
    return jsonify({
        "neighbourhood_cleansed": name,
        "message": f"Barrio recibido correctamente: {name}"
    })


# RUTA CON PARÁMETROS DE LA QUERY PARA USAR LA FUNCIÓN DE PREDICCIÓN
# Recibe los datos que necesita el modelo para hacer las predicciones

def build_model_input(data_source):
    data = {col: 0 for col in MODEL_COLUMNS}

    try:
        data["minimum_nights"] = float(data_source.get("minimum_nights", 0))
        data["number_of_reviews"] = float(data_source.get("number_of_reviews", 0))
        data["availability_365"] = float(data_source.get("availability_365", 0))
    except (TypeError, ValueError):
        raise ValueError(
            "minimum_nights, number_of_reviews y availability_365 deben ser numéricos"
        )

    neighbourhood = data_source.get("neighbourhood")
    room_type = data_source.get("room_type")

    if not neighbourhood:
        raise ValueError("Falta el parámetro 'neighbourhood'")
    if not room_type:
        raise ValueError("Falta el parámetro 'room_type'")

    if neighbourhood not in VALID_NEIGHBOURHOODS:
        raise ValueError(
            f"Barrio no válido. Usa uno de estos: {', '.join(VALID_NEIGHBOURHOODS)}"
        )

    if room_type not in VALID_ROOM_TYPES:
        raise ValueError(
            f"room_type no válido. Usa uno de estos: {', '.join(VALID_ROOM_TYPES)}"
        )

    neighbourhood_col = f"neighbourhood_{neighbourhood}"
    room_type_col = f"room_type_{room_type}"

    data[neighbourhood_col] = 1
    data[room_type_col] = 1

    return data






# PREDICCION DE RESULTADOS
# /predict_query?neighbourhood=Sol&room_type=Entire%20home/apt&minimum_nights=5...
@app.route("/predict_query", methods=["GET"])
def predict_query():
    try:
        input_data = build_model_input(request.args)
        df = pd.DataFrame([input_data], columns=MODEL_COLUMNS)
        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_price": float(prediction),
            "input": {
                "neighbourhood": request.args.get("neighbourhood"),
                "room_type": request.args.get("room_type"),
                "minimum_nights": request.args.get("minimum_nights"),
                "number_of_reviews": request.args.get("number_of_reviews"),
                "availability_365": request.args.get("availability_365")
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_data = build_model_input(data)
        df = pd.DataFrame([input_data], columns=MODEL_COLUMNS)
        prediction = model.predict(df)[0]

        return jsonify({
            "predicted_price": float(prediction),
            "input": data
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

