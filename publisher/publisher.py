from time import sleep

import paho.mqtt.publish as publish

HOST = 'mqtt'
PORT = 1883
TOPIC = 'cosn'

while True:
    publish.single(topic=TOPIC, payload="Hey ho!", hostname=HOST, port=PORT)
    sleep(1)