import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Conectado con mqtt "+str(rc))


def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic + " " + str(msg.payload))
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("data Recived type", type(m_decode))
    print("data Recived", m_decode)
    print("Converting from Json to Object")
    m_in = json.loads(m_decode)
    print(type(m_in))
    print("data_to_send = ", m_in["data_to_send"])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.subscribe("ETSISI/#/3104")


client.loop_forever()
