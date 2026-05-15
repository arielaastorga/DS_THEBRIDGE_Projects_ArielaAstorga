# Importamos pickle para poder cargar el archivo model.pkl
import pickle

# Importamos Flask para crear la API,
# jsonify para devolver respuestas en formato JSON,
# y request para leer datos que envía el usuario
from flask import Flask, jsonify, request

# Creamos la aplicación Flask
# __name__ le indica a Flask dónde está el archivo principal
app = Flask(__name__)

# Esto activa el modo debug, muestra errores más detallados cuando estoy programando
app.config["DEBUG"] = True


# Cargamos el "modelo" al iniciar la aplicación
# Esto hace que el modelo se lea una sola vez al arrancar la API
# y no en cada petición
with open("model.pkl", "rb") as f:
    model = pickle.load(f)


# Ruta principal de la API
# Se ejecuta cuando alguien entra a la URL raíz "/"
# En la terminal bash:   http://localhost:5000/
# En render:  https://tu-api.onrender.com/

@app.route("/", methods=["GET"])
def home():
    # Devolvemos un mensaje en formato JSON
    return jsonify({
        "message": "API Flask para predicción de precio de apartamentos"
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
        "neighbourhood": name,
        "message": f"Barrio recibido correctamente: {name}"
    })


# RUTA CON PARÁMETROS DE LA QUERY PARA USAR LA FUNCIÓN DE PREDICCIÓN
# Recibe los datos que necesita el modelo para hacer las predicciones
# Variables del modelo:
'''
neighbourhood
room_type
minimum_nights
number_of_reviews 
availability_365  
number_of_reviews_ltm

variable objetivo: price 
'''

# Ejemplo:
# /predict_query?neighbourhood=Sol&room_type=Entire%20home/apt&minimum_nights=5...
@app.route("/predict_query", methods=["GET"])
def predict_query():
    try:
        # request.args.get(...) lee parámetros que vienen en la URL
        neighbourhood = request.args.get("neighbourhood")
        room_type = request.args.get("room_type")

        # Convertimos las variables numéricas a float, porque llegan como texto desde la URL
        minimum_nights = float(request.args.get("minimum_nights"))
        number_of_reviews = float(request.args.get("number_of_reviews"))
        availability_365 = float(request.args.get("availability_365"))
        number_of_reviews_ltm = float(request.args.get("number_of_reviews_ltm"))

        # Llamamos al método predict_one de nuestro modelo pasándole todas las variables necesarias
        prediction = model.predict_one(
            neighbourhood = neighbourhood,
            room_type = room_type,
            minimum_nights = minimum_nights,
            number_of_reviews = number_of_reviews,
            availability_365 = availability_365,
            number_of_reviews_ltm = number_of_reviews_ltm
        )

        # Devolvemos la predicción y también los datos de entrada
        return jsonify({
            "predicted_price": prediction,
            "input": {
                "neighbourhood": neighbourhood,
                "room_type": room_type,
                "minimum_nights": minimum_nights,
                "number_of_reviews": number_of_reviews,
                "availability_365": availability_365,
                "number_of_reviews_ltm": number_of_reviews_ltm
            }
        })

    except Exception as e:
        # Si hay cualquier error, devolvemos un JSON con el mensaje de error 
        # y un código HTTP 400 (bad request)
        return jsonify({
            "error": str(e)
        }), 400



# Ruta que recibe datos en el body en formato JSON por parte del 'cliente'
# Con POST
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # request.get_json() intenta leer el cuerpo de la petición como JSON
        # Para que funcione bien, el cliente debe enviar:
        # Content-Type: application/json
        data = request.get_json()

        # Extraemos cada valor del JSON recibido
        neighbourhood = data["neighbourhood"]
        room_type = data["room_type"]

        # Convertimos a float las variables numéricas
        minimum_nights = float(data["minimum_nights"])
        number_of_reviews = float(data["number_of_reviews"])
        availability_365 = float(data["availability_365"])
        number_of_reviews_ltm = float(data["number_of_reviews_ltm"])

        # Llamamos al modelo para obtener la predicción
        prediction = model.predict_one(
            neighbourhood=neighbourhood,
            room_type=room_type,
            minimum_nights=minimum_nights,
            number_of_reviews=number_of_reviews,
            availability_365=availability_365,
            number_of_reviews_ltm=number_of_reviews_ltm
        )

        # Devolvemos el precio predicho y los datos recibidos
        return jsonify({
            "predicted_price": prediction,
            "input": data
        })

    except Exception as e:
        # Si algo falla, devolvemos el error en JSON
        return jsonify({
            "error": str(e)
        }), 400


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

'''
# Este bloque solo se ejecuta si lanzas el archivo con:
# python app.py
# Sirve para desarrollo local
if __name__ == "__main__":
    app.run(debug=True)
'''
