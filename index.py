import time
import json
from datetime import datetime
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
lights = dict(
    L1=18,
    B1=23
)

actions = dict(
    ON=True,
    OFF=False
)

for l in lights:
    GPIO.setup(lights[l], GPIO.OUT)
    
def process_message(msg):
    data = json.loads(msg)
    try:
        action = data.get('action', None)
        light = data.get('light', None)
        if light in lights and action in actions:
            GPIO.output(lights[light], actions[action])
    except e:
        print("Error performing action due to ", e.message)

def on_connect(client, data, flags, rc):
    print("CONNACK received with code %d" % (rc))
    client.subscribe("/smarthouse/duke/houselights")

def on_message(client, userdata, msg):
    print("received", msg.topic + " "+str(msg.payload))
    process_message(msg)

def on_publish(client, data, mid):
    print("published", str(mid))

client = mqtt.Client("rasp4b", True, None, mqtt.MQTTv31)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set("duke__", "dukeHiveMQ8")
client.connect("3221fc9b1a7e4e76ad7cce10b8489e96.s1.eu.hivemq.cloud", 8883, 60)
client.loop_start()
