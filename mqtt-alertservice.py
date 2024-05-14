import paho.mqtt.client as mqtt
import smtplib
from email.mime.text import MIMEText

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
password = 'Enviaralerta123'
destinatario = 'recibiralertas@gmail.com'
asunto = 'Alerta importante'
mensajePrueba = 'Este es un mensaje de alerta importante.'

# Detalles del servidor SMTP de Gmail
servidor_smtp = 'smtp.gmail.com'
puerto_smtp = 587  # El puerto para TLS

def enviar_alerta(destinatario, asunto, mensaje, remitente, password, servidor_smtp, puerto_smtp):
    # Crear mensaje MIME
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    # Iniciar conexión SMTP
    try:
        server = smtplib.SMTP(servidor_smtp, puerto_smtp)
        server.starttls()
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


# Llamada a la función para enviar el correo
enviar_alerta(destinatario, asunto, mensajePrueba, remitente, password, servidor_smtp, puerto_smtp)

def on_message(client, userdata, msg):
    print("Recibido: " + msg.topic+" "+str(msg.payload))
    ##
    mensaje ="ha llegado un dato"
    enviar_alerta(destinatario, asunto, mensaje, remitente, password, servidor_smtp, puerto_smtp)


client.on_message = on_message

#Bloqueo de llamadas que procesa el tráfico de la red, envía callbacks y gestiona las reconectando.
#Hay disponibles otras funciones de bucle * () que proporcionan una interfaz de hebras y un interfaz manual.
client.loop_forever()