import paho.mqtt.client as mqtt
import time

import utils

air_conditioner_flag = False

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))

    global air_conditioner_flag
    if message == "420;1":
        print("Turning humidifier on.")

        return
    elif message == "420;-1":
        print("Turning humidifier off.")

        return
    elif message == "690;1":
        air_conditioner_flag = True
    
        print("Turning air conditioner on.")

        return
    elif message == "690;-1":
        air_conditioner_flag = False
        
        print("Turning air conditioner off.")

        return

    temperature, humidifier = message.split(";")

    humidifier_status = "unchanged"

    humidifier =  int(humidifier)
    temperature = int(temperature)

    if humidifier == -1:
        humidifier_status = "off"
    elif humidifier == 1:
        humidifier_status = "on"

    if temperature > -1 and air_conditioner_flag:
        print(f"Setting air conditioner to {temperature}°C.")

    if humidifier_status != "unchanged":
        print("Turning humidifier " + humidifier_status + ".")

if __name__ == "__main__":
    client = mqtt.Client("Projeto_3")
    client.connect(utils.TOPIC) 

    print("Connected!")

    client.loop_start()

    while True:
        client.subscribe("henriqueblang/gadgets")
        client.on_message = on_message 

    client.loop_stop()