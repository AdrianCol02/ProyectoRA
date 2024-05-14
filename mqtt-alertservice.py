import paho.mqtt.client as mqtt
import smtplib
from email.mime.text import MIMEText
import json


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.connect("10.100.0.105", 1883, 60)

#La callback para cuando el cliente recibe una respuesta CONNACK del servidor
def on_connect(client, userdata, flags, rc, properties):
    print("Conectado con mqtt "+str(rc))

client.on_connect = on_connect

client.subscribe("/get")
client.subscribe("/post")

# Detalles de configuración del correo
remitente = 'enviaralerta@gmail.com'
password = 'lmoslagycfvyhhiq'
destinatario = 'alertarecibir@gmail.com'
asunto = 'Alerta importante'
mensajePrueba = 'Este es un mensaje de alerta importante.'

# Detalles del servidor SMTP de Gmail
servidor_smtp = 'smtp.gmail.com'
puerto_smtp = 465  # El puerto para TLS


def enviar_alerta(destinatario, asunto, mensaje, remitente, password, servidor_smtp, puerto_smtp):
    # Crear mensaje MIME
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    # Iniciar conexión SMTP
    try:
        server = smtplib.SMTP_SSL(servidor_smtp, puerto_smtp)
        server.ehlo()
        # Autenticarse con el servidor SMTP
        server.login(remitente, password)
        # Enviar el correo electrónico
        server.sendmail(remitente, destinatario, msg.as_string())
        print("Correo enviado correctamente")
    except Exception as e:
        print(f"No se pudo enviar el correo. Error: {e}")
    finally:
        # Cerrar la conexión SMTP
        server.quit()


def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic+" "+str(msg.payload))

    datos = json.loads(msg.payload.decode())
    #datos_formateados = json.dumps(datos, indent=4)

    nodo = datos['id_nodo']
    temp = float(datos['temperatura'])
    humedad = float(datos['humedad'])
    co2 = float(datos['co2'])
    volatiles = float(datos['volatiles'])
    timestamp = datos['timestamp']


    if(temp > 29):
        #mensaje = "Ha llegado el dato:\n" + datos_formateados + '\nLa temperatura es demasiado alta. Se recomienda bajar a 20.'
        mensaje = f"Temperatura actual: {temp}°C\n" \
                  f"\nLa temperatura es demasiado alta. Se recomienda bajar a 20°C."
        enviar_alerta(destinatario, asunto, mensaje, remitente, password, servidor_smtp, puerto_smtp)


client.on_message = on_message

#Bloqueo de llamadas que procesa el tráfico de la red, envía callbacks y gestiona las reconectando.
#Hay disponibles otras funciones de bucle * () que proporcionan una interfaz de hebras y un interfaz manual.
client.loop_forever()