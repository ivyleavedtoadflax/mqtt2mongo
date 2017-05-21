import paho.mqtt.client as mqtt
from datetime import datetime
import os

# Debug stuff
#print('{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.now()))
#print(os.environ.get('MQTT_HOST'))
#print(os.environ.get('MQTT_PORT'))
#print(os.environ.get('MQTT_USERNAME'))
#print(os.environ.get('MQTT_PASSWORD'))
#print(os.environ.get('MQTT_TOPIC'))


# The callback for when the client receives a a
# CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.username_pw_set(username=os.environ.get('MQTT_USERNAME'),
            password=os.environ.get('MQTT_PASSWORD'))
    client.subscribe(os.environ.get('MQTT_TOPIC'))
    
    # The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    
    post = {
            "timestamp": '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.now()),
            "topic": os.environ.get('MQTT_TOPIC'),
            "soil" : 999
            }

    print(post)
    
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
    
client.connect(
        os.environ.get('MQTT_HOST'), 
        int(os.environ.get('MQTT_PORT')), 
        60
        )
    
client.loop_forever()
