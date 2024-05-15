from flask import Flask, request, jsonify
import threading
import time
import queue

app = Flask(__name__)
bucket = queue.Queue(maxsize=5)  # Tamaño del bucket

def leaky_bucket():
     while True:
         if not bucket.empty():
             request_data = bucket.get()
             # Aquí puedes realizar la lógica de reenvío a otro puerto
             print("Reenviando solicitud:", request_data)
         time.sleep(1)  # Controla la velocidad del bucket

@app.route('/', methods=['GET', 'POST'])
def handle_request():
     if request.method == 'GET' or request.method == 'POST':
         if bucket.full():
             return jsonify({"message": "Too Many Requests"}), 429
         bucket.put(request.data)
         return jsonify({"message": "Request Received"}), 200

if __name__ == '__main__':
     # Inicia el hilo del leaky bucket
     bucket_thread = threading.Thread(target=leaky_bucket)
     bucket_thread.daemon = True
     bucket_thread.start()

     # Inicia el servidor Flask
     app.run(port=5000)
