import random
from paho.mqtt import client as paho
from dotenv import dotenv_values

import serial
import Rpi.GPIO as GPIO

config = dotenv_values('.env')

# mqtt broker setup
host = config.get('HOST')
port = int(config.get('PORT'))

client_id = f'psi_responsi-{random.random()}'

# 'DEV' for testing using dummy data
# 'PROD' for running the system using real data
MODE = 'DEV'


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # MQ Pin
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.OUT)

    return serial.Serial('ttyUSB0', 9600)


def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print('Connect Succesfully')
    else:
        print('Connect failed')


def connect_handler(onConnect_cb, host, port):
    client = paho.Client(client_id, protocol=paho.MQTTv5,
                         transport='websockets')
    client.on_connect = onConnect_cb
    client.connect(host, port)
    return client


def publish_handler(client):

    io = setup()

    while True:
        cleaned_data = []

        if MODE == 'PROD':
            cleaned_data = io.readline().decode().rstrip().split('#')
        elif MODE == 'DEV':
            cleaned_data = [
                random.randint(20, 45),
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(170, 230),
                random.randint(0, 1),
                random.randint(0, 1)
            ]

        isGas = GPIO.input(15)
        cleaned_data.append(isGas)

        if isGas == 0:
            GPIO.output(16, GPIO.HIGH)
        else:
            GPIO.output(16, GPIO.LOW)

        if(len(cleaned_data) == 6):
            data_msg = {
                'responsi/data/aktuator/temperature': cleaned_data[0],
                'responsi/data/aktuator/lpgTotal': cleaned_data[1],
                'responsi/data/aktuator/numberOfSample': cleaned_data[2],
                'responsi/data/aktuator/Mass': cleaned_data[3],
                'responsi/data/aktuator/isStop': cleaned_data[4],
                'responsi/data/aktuator/isGas': cleaned_data[5],
            }

            for topic, msg in data_msg.items():
                result = client.publish(topic=topic, payload=msg)
                if(result[0] == 0):
                    print(f'{msg} has been succesfully sending to {topic}')
                else:
                    print('sending failed.')


if __name__ == '__main__':
    client = connect_handler(on_connect, host, port)
    client.loop_start()

    publish_handler(client)
