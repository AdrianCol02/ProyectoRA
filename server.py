from flask import Flask, jsonify, request
import os
from datetime import datetime
import paho.mqtt.client as mqtt

"""""
#La callback para cuando el cliente recibe una respuesta CONNACK del servidor
def on_connect(client, userdata, flags, rc):
    print("Conectado con mqtt "+str(rc))
Hola

#La callback para cuando se recibe un mensaje PUBLICAR desde el servidor.
def on_publish(client, userdata, mid):
    print("Mensaje publicado")

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect("test.mosquitto.org", 1883, 60)

#Publico un primer mensaje
"""""
app = Flask (__name__)


@app.route("/ping")
def ping():
    return jsonify({"message": "HOLA!"})


@app.route('/get', methods=['GET'])
def addDatoGet():
    # Obtener los parámetros de la URL
    id_nodo = request.args.get('id_nodo')
    temperatura = request.args.get('temperatura')
    humedad = request.args.get('humedad')
    co2 = request.args.get('co2')
    volatiles = request.args.get('volatiles')

    # Obtener la fecha y hora actual
    now = datetime.now()

    # Construir el nombre del archivo de registro
    logfile_name = f"public/logs/{id_nodo}-{now.year}-{now.month}-{now.day}.csv"

    # Comprobar si el archivo ya existe
    if os.path.exists(logfile_name):
        # Si el archivo existe, agregar la línea de datos
        content = f"{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"
    else:
        # Si el archivo no existe, agregar la línea de encabezado seguida de los datos
        content = f"id_nodo;timestamp;temperatura;humedad;CO2;volatiles\n{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"

    # Agregar el contenido al archivo de registro
    append_to_file(logfile_name, content)

    # Devolver una respuesta indicando que los datos se han guardado
    return f"Saving: {content} in: {logfile_name}"


@app.route('/post', methods=['POST'])
def addDatoPost():
    # Obtener los datos del formulario enviado por POST
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
        # Si el archivo existe, agregar la línea de datos
        content = f"{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"
    else:
        # Si el archivo no existe, agregar la línea de encabezado seguida de los datos
        content = f"id_nodo;timestamp;temperatura;humedad;CO2;volatiles\n{id_nodo};{now.timestamp()};{temperatura};{humedad};{co2};{volatiles}\n"

    # Agregar el contenido al archivo de registro
    append_to_file(logfile_name, content)

    # Devolver una respuesta indicando que los datos se han guardado
    return f"Saving: {content} in: {logfile_name}"

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

app.run (debug=True, port=4000)
