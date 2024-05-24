from flask import Flask, jsonify, request
import requests
import time
from threading import Lock

app = Flask(__name__)

# Configuración del Leaky Bucket
bucket_capacity = 100
# Capacidad del cubo
leak_rate = 1
# Número de tokens que se filtran por segundo
tokens = bucket_capacity
# Inicialmente el cubo está lleno
last_check = time.time()
lock = Lock()

# Lista negra de IPs
blacklist = set()
blacklist.add("10.0.4.32")

# Verifica si hay suficientes tokens en el cubo
def allow_request():
     global tokens, last_check
     current_time = time.time()
     time_passed = current_time - last_check
     last_check = current_time

     # Filtra tokens de acuerdo a la tasa de fuga
     tokens = min(bucket_capacity, tokens + time_passed * leak_rate)
     if tokens >= 1:
         tokens -= 1
         return True
     else:
         return False

def is_blacklisted(ip):
    return ip in blacklist

# Rutas para gestionar las peticiones
@app.route('/ping')
def ping():
     return jsonify({"message": "HOLA!"})

@app.route('/', methods=['GET'])
def handle_get():
    client_ip = request.remote_addr
    if is_blacklisted(client_ip):
        return jsonify({"error": "Forbidden"}), 403

    with lock:
         if not allow_request():
             return jsonify({"error": "Too many requests"}), 429

     # Obtener los parámetros de la URL
    params = request.args

    #Reenviar la solicitud GET al puerto 4002
    response = requests.get('http://localhost:4002/', params=params)
    return response.content, response.status_code

@app.route('/', methods=['POST'])
def handle_post():
    client_ip = request.remote_addr
    if is_blacklisted(client_ip):
        return jsonify({"error": "Forbidden"}), 403

    with lock:
         if not allow_request():
             return jsonify({"error": "Too many requests"}), 429

    #Obtener los datos JSON del cuerpo de la solicitud
    data = request.json

    # Reenviar la solicitud POST al puerto 4002
    response = requests.post('http://localhost:4002/', json=data)
    return response.content, response.status_code


@app.route('/blacklistin', methods=['GET'])
def add_to_blacklist():
    ip = request.args.get('ip')
    if ip in blacklist:
        return jsonify({"error": f"La IP {ip} ya está en la blacklist"}), 400
    else:
        blacklist.add(ip)
        return jsonify({"mensaje": f"La IP {ip} fue añadida correctamente"}), 200


@app.route('/blacklistout', methods=['GET'])
def remove_from_blacklist():
    ip = request.args.get('ip')
    if ip in blacklist:
        blacklist.remove(ip)
        return jsonify({"message": f"IP {ip} eliminada correctamente"}), 200
    else:
        return jsonify({"error": f"La IP {ip} no está en la blacklist"}), 400


# Ejecutar la aplicación Flask
if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=4003)
