import paho.mqtt.client as paho
from paho import mqtt
import time


#_____________________________________________________________
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"\n\nConnected with result code: {rc}")
    client.subscribe(c_topic, qos=1)
    client.subscribe(noti_topic, qos=1)


def on_message(client, userdata, msg):
    client_id = client._client_id.decode('utf-8')
    topic = msg.topic

    message = msg.payload.decode()
    print(f"\nReceived message: ({message}) on topic {topic}")
    
    if topic == c_topic:
        time.sleep(2)
        print(f"\nReceived message: ({message}) on topic {topic}")
        client.publish(s_topic, f"Message from {client_id} \n")
        
    else:
        print("Waiting message from Client...\n")

#______________________________________________________________
broker = "47bf355a84b543c9b3d10e2cbb9b2ba7.s1.eu.hivemq.cloud"
port = 8883
username = "Server_Ter"
password = "Dkien246@#"
ca_cert_path = "isrgrootx1.pem" 

noti_topic = "test/noti"
s_topic = "test/server"
c_topic = "test/client"
#______________________________________________________________


# Setup server
client = paho.Client(client_id="Server_Ter", userdata=None, protocol=paho.MQTTv5)
client.on_message = on_message
client.on_connect = on_connect
client.tls_set(ca_cert_path, tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)

# Connect with HiveMQ broker
client.connect(broker, port)

client.publish(noti_topic, "Start")



client.loop_forever()
