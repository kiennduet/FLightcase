import paho.mqtt.client as paho
from paho import mqtt
import time

broker = "47bf355a84b543c9b3d10e2cbb9b2ba7.s1.eu.hivemq.cloud"
port = 8883
username = "Client1_Ter"
password = "Dkien246@#"
ca_cert_path = "isrgrootx1.pem"

noti_topic = "test/noti"
s_topic = "test/server"
c_topic = "test/client"

#______________________________________________________________
def decode_message(message):
    parts = message.split(':')
    label = parts[0].strip('"').strip()
    value = float(parts[1].strip('"').strip())
    return label, value

def on_connect(client, userdata, flags, rc, properties=None):
   print(f"\n\nConnected with result code: {rc}\n")
   client.subscribe(noti_topic, qos=1)
   client.subscribe(s_topic, qos=1)

def on_message(client, userdata, msg):
    client_id = client._client_id.decode('utf-8')
    message = msg.payload.decode()
    topic = msg.topic

    if message == "Start":
        print("Start sending...")
        client.publish(c_topic, f"Message from {client_id}\n")
    else:
        print(message)

    if topic == s_topic:
        time.sleep(5)
        client.publish(c_topic, f"Message from {client_id}\n")
    else:
        print(f"Received message: ({message}) on topic {topic}\n")
        print(f"Waiting message form Server...\n")

    # label, value = decode_message(message)
    
  

client = paho.Client(client_id="Client1_Ter", userdata=None, protocol=paho.MQTTv5)
client.on_message = on_message
client.on_connect = on_connect

client.tls_set(ca_cert_path, tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)
client.connect(broker, port)

client.loop_forever()
