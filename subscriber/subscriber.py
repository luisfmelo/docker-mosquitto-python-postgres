import os

import paho.mqtt.client as paho
import psycopg2 as psycopg2

cur = None


def save_message(topic, qos, message):
    query = """
        INSERT INTO public.mosquitto_logs (id, timestamp, topic, message, qos) VALUES (DEFAULT, now(), '{}', '{}', '{}');
    """.format(topic, str(message.decode()), str(qos))

    cur.execute(query)


def connect_db():
    try:
        conn = psycopg2.connect(host="db",
                                database=os.environ["POSTGRES_DB"],
                                user=os.environ["POSTGRES_USER"],
                                password=os.environ["POSTGRES_PASSWORD"])
        conn.autocommit = True

    except:
        print("I am unable to connect to the database")
        return None

    cursor = conn.cursor()

    # Create Log Table if not exist
    query = """
        CREATE TABLE IF NOT EXISTS public.mosquitto_logs (
            id serial primary key,
            timestamp timestamp,
            topic VARCHAR(256),
            message TEXT,
            qos VARCHAR(16)
        );
    """

    cursor.execute(query)

    return cursor


def on_message(client, userdata, msg):
    print("%-20s %d %s" % (msg.topic, msg.qos, msg.payload))
    client.publish('pong', 'ack', 0)
    save_message(msg.topic, msg.qos, msg.payload)


if __name__ == '__main__':
    print(os.environ)
    # Set up database connection
    cur = connect_db()

    client = paho.Client()
    client.on_message = on_message
    client.connect(os.environ['MOSQUITTO_HOST'], int(os.environ['MOSQUITTO_PORT']))
    client.subscribe(os.environ['MOSQUITTO_TOPIC'], qos=2)
    client.loop_forever()
