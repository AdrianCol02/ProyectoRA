import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
    print("Conectado con mqtt "+str(rc))


def on_publish(client, userdata, mid):
    print("Mensaje publicado")


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish


client.connect("test.mosquitto.org", 1883, 60)

send_msg = {
    'data_to_send': "v1",
    'also_send_this': "v2"
}

client.publish("ETSISI/Adrian")
client.loop_forever()
