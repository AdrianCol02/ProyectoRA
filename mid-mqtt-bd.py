import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient

client_mongo = MongoClient('localhost', 27017)
db = client_mongo['mongodb-105']  # Reemplaza 'mi_base_de_datos' con el nombre de tu base de datos
nodos = db['nodos']  # Reemplaza 'mi_coleccion' con el nombre de tu colección


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect("10.100.0.105", 1883, 60)

#La callback para cuando el cliente recibe una respuesta CONNACK del servidor
def on_connect(client, userdata, flags, rc, properties):
    print("Conectado con mqtt "+str(rc))

client.on_connect = on_connect

client.subscribe("/nodos")

#La callback para cuando se recibe un mensaje PUBLICAR desde el servidor.
def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic+" "+str(msg.payload))
    try:
        # Decodificar el mensaje JSON
        json_data = json.loads(msg.payload.decode("utf-8"))

        # Insertar el JSON en la colección de MongoDB
        nodos.insert_one(json_data)

        print("JSON insertado en MongoDB exitosamente.")
    except Exception as e:
        print("Error al insertar el JSON en MongoDB:", e)
    return 0


client.on_message = on_message

#Bloqueo de llamadas que procesa el tráfico de la red, envía callbacks y gestiona las reconectando.
#Hay disponibles otras funciones de bucle * () que proporcionan una interfaz de hebras y un interfaz manual.
client.loop_forever()
