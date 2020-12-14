import paho.mqtt.client as mqtt
import time

import utils

'''
def on_message(client, userdata, message):
    print("received message: " , str(message.payload.decode("utf-8")))

mqttBroker ="test.mosquitto.org"

client = mqtt.Client("smartphone")
client.connect(mqttBroker) 
client.loop_start()

while True:
    client.subscribe("henriqueblang")
    client.on_message=on_message 

client.loop_stop()
'''

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))

    humidifier, temperature = message.split(";")

    humidifier_status = "unchanged"

    humidifier = int(humidifier)
    if humidifier == -1:
        humidifier_status = "off"
    elif humidifier == 1:
        humidifier_status = "on"

    print(f"[uploader] Received humidifier: {humidifier_status}, temperature: {temperature}")

    print("Setting air conditioner to " + temperature + "°C.")

    if humidifier_status != "unchanged":
        print("Turning humidifier " + humidifier_status + ".")

if __name__ == "__main__":
    client = mqtt.Client("Projeto")
    client.connect(utils.TOPIC) 

    print("Connected!")

    client.loop_start()

    while True:
        client.subscribe("henriqueblang/gadgets")
        client.on_message = on_message 

    client.loop_stop()