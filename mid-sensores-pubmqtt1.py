from flask import Flask, jsonify, request
import os
from datetime import datetime
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")

# The callback for when a PUBLISH message is received from the server.
def on_message(mqttc, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("10.100.0.105", 1883, 60)

mqttc.loop_start()

app = Flask (__name__)


@app.route("/ping")
def ping():
    return jsonify({"message": "HOLA!"})


@app.route('/', methods=['GET'])
def addDatoGet():
    # Obtener los parámetros de la URL
    id_nodo = request.args.get('id_nodo')
    temperatura = request.args.get('temperatura')
    humedad = request.args.get('humedad')
    co2 = request.args.get('co2')
    volatiles = request.args.get('volatiles')

    # Obtener la fecha y hora actual
    now = datetime.now()

    data = {
        'id_nodo': id_nodo,
        'temperatura': temperatura,
        'humedad': humedad,
        'co2': co2,
        'volatiles': volatiles,
        'timestamp': now.strftime("%Y-%m-%d %H:%M:%S")
    }

    json_data = jsonify(data).get_data(as_text=True)

    # Construir el nombre del archivo de registro
    #logfile_name = f"get/{id_nodo}-{temperatura}-{humedad}-{co2}-{volatiles}-{now.year}-{now.month}-{now.day}"

    msg_info = mqttc.publish("/nodos", json_data, qos=1)

    return f"Saving: {id_nodo}"

@app.route('/', methods=['POST'])
def addDatoPost():

    data = request.json

    msg_info = mqttc.publish("/nodos", data, qos=1)


    # Devolver una respuesta indicando que los datos se han guardado
    return f"Saving:"

# Función para agregar contenido a un archivo
def append_to_file(file_to_append, content):
    with open(file_to_append, 'a') as file:
        file.write(content)

# Rutas para servir archivos estáticos y listarlos
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/users')
def users():
    return app.send_static_file('users.html')

@app.route('/logs')
def logs():
    return jsonify(os.listdir('public/logs'))

# Para servir los archivos estáticos
@app.route('/logs/<path:filename>')
def serve_logs(filename):
    return app.send_static_file(os.path.join('logs', filename))

# Manejador para errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# Manejador para errores 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

app.run (debug=True, host ="10.100.0.105", port=4000)