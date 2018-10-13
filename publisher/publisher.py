import os
import random
from time import sleep

import paho.mqtt.publish as publish

messages = [
    'Hey Ho!',
    'Hi there',
    'Wuzup?',
    'Hello',
    'Nice to meet you'
]

while True:
    publish.single(
        topic=os.environ['MOSQUITTO_TOPIC'],
        payload=random.choice(messages),
        hostname=os.environ['MOSQUITTO_HOST'],
        port=int(os.environ['MOSQUITTO_PORT'])
    )
    sleep(1)
