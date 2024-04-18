from flask import Flask, jsonify, request
import os
from datetime import datetime
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Configuración de MQTT
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Conectado con el código de resultado {reason_code}")
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

mqttc = mqtt.Client(client_id="flask_client", clean_session=True)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.100.0.105", 4000)
mqttc.loop_start()

# Función auxiliar para agregar contenido a un archivo
def append_to_file(file_to_append, content):
    with open(file_to_append, 'a') as file:
        file.write(content)

@app.route("/ping")
def ping():
    return jsonify({"message": "HOLA!"})

@app.route('/get', methods=['GET'])
def addDatoGet():
    # Obtener parámetros de la URL
    id_nodo = request.args.get('id_nodo')
    temperatura = request.args.get('temperatura')
    humedad = request.args.get('humedad')
    co2 = request.args.get('co2')
    volatiles = request.args.get('volatiles')

    # Obtener la fecha y hora actual
    now = datetime.now()

    # Construir el nombre del archivo de registro
    logfile_name = f"get/{id_nodo}-{temperatura}-{humedad}-{co2}-{volatiles}-{now.year}-{now.month}-{now.day}.csv"

    # Publicar en el tema MQTT
    mqttc.publish("/get", logfile_name, qos=1)

    # Comprobar si el archivo ya existe
    if os.path.exists(logfile_name):
        content = f"{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"
    else:
        content = f"id_nodo;timestamp;temperatura;humedad;CO2;volatiles\n{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"

    # Agregar el contenido al archivo
    append_to_file(logfile_name, content)

    return f"Guardando: {content} en: {logfile_name}"

@app.route('/post', methods=['POST'])
def addDatoPost():
    # Obtener datos del formulario enviado por POST
    id_nodo = request.form.get('id_nodo')
    temperatura = request.form.get('temperatura')
    humedad = request.form.get('humedad')
    co2 = request.form.get('co2')
    volatiles = request.form.get('volatiles')

    # Obtener la fecha y hora actual
    now = datetime.now()

    # Construir el nombre del archivo de registro
    logfile_name = f"public/logs/{id_nodo}-{now.year}-{now.month}-{now.day}.csv"

    # Comprobar si el archivo ya existe
    if os.path.exists(logfile_name):
        content = f"{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"
    else:
        content = f"id_nodo;timestamp;temperatura;humedad;CO2;volatiles\n{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"

    # Agregar el contenido al archivo
    append_to_file(logfile_name, content)

    return f"Guardando: {content} en: {logfile_name}"

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/users')
def users():
    return app.send_static_file('users.html')

@app.route('/logs')
def logs():
    return jsonify(os.listdir('public/logs'))

@app.route('/logs/<path:filename>')
def serve_logs(filename):
    return app.send_static_file(os.path.join('logs', filename))

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'No encontrado'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == "__main__":
    app.run(debug=True, host="10.100.0.105", port=4000)
