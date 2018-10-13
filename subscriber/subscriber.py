import os

import paho.mqtt.client as paho
import psycopg2 as psycopg2

HOST = 'mqtt'
PORT = 1883
TOPIC = 'cosn'
cur = None

def connect_db():
    conn = psycopg2.connect(host="db",
                            database=os.environ["POSTGRES_DB"],
                            user=os.environ["POSTGRES_USER"],
                            password=os.environ["POSTGRES_PASSWORD"])
    cursor = conn.cursor()

    return cursor

def on_message(client, userdata, msg):
    print("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    client.publish('pong', 'ack', 0)


if __name__ == '__main__':
    print(os.environ)
    # Set up database connection
    cur = connect_db()

    client = paho.Client()
    client.on_message = on_message
    client.connect(HOST, PORT).subscribe(TOPIC, qos=2).loop_forever()
