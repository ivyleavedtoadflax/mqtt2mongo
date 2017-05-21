import paho.mqtt.client as mqtt
from datetime import datetime
import os
import pymongo

# Define MongoClient

client = pymongo.MongoClient(
        os.environ.get('MONGO_HOST'),
        int(os.environ.get('MONGO_PORT'))
        )
db = client.test
coll = db.test_collection

# Debug stuff
#print('{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.now()))
#print(os.environ.get('MQTT_HOST'))
#print(os.environ.get('MQTT_PORT'))
#print(os.environ.get('MQTT_USERNAME'))
#print(os.environ.get('MQTT_PASSWORD'))
#print(os.environ.get('MQTT_TOPIC'))
#print(os.environ.get('MONGO_HOST'))
#print(os.environ.get('MONGO_PORT'))


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
            "topic": msg._topic.decode("utf-8") ,
            "value" : msg.payload.decode("utf-8").strip() 
            }

    post_id = coll.insert_one(post).inserted_id
    
    print('Inserted in mongo at: ', post_id)
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
