import paho.mqtt.client as mqtt
import serial
import time
msg_counter=0

ser=serial.Serial('/dev/ttyTHS2', 38400,timeout = 0.5)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("hmd")


def on_message(client, userdata, msg):
    global msg_counter
    msg_counter=msg_counter+1
    if msg_counter%2==0:
        positions =  msg.payload.decode()
        print(positions)
        ser.write(msg.payload)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("10.2.9.223", 1883, 60)
client.loop_forever()
