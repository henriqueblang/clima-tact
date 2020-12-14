import paho.mqtt.client as mqtt
import time

import utils

weather_data = []

last_ac_temperature = None
last_humidifier_status = None

aux_client = mqtt.Client("Projeto_4")
aux_client.connect(utils.TOPIC)

def on_message(client, userdata, message):
    message = str(message.payload.decode("utf-8"))

    humidity, temperature = message.split(";")

    humidity =    float(humidity)
    temperature = float(temperature)

    print(f"[processor] Received humidity: {humidity}, temperature: {temperature}")

    weather_data.append((humidity, temperature))

    if len(weather_data) < utils.DATA_PROCESS_AMOUNT:
        return

    mean_humidity = 0
    mean_temperature = 0

    for weather_pair in weather_data:
        mean_humidity += weather_pair[0]
        mean_temperature += weather_pair[1]

    mean_humidity /= utils.DATA_PROCESS_AMOUNT
    mean_temperature /= utils.DATA_PROCESS_AMOUNT

    ac_temperature = round(utils.AIR_CONDITIONER_PERCENTAGE * mean_temperature)

    global last_ac_temperature
    if last_ac_temperature is None:
        last_ac_temperature = ac_temperature + 1

    step = last_ac_temperature < ac_temperature and 1 or -1
    ac_linear_temperatures = [i for i in range(last_ac_temperature + step, ac_temperature + step, step)]

    for temperature in ac_linear_temperatures:
        aux_client.publish("henriqueblang/gadgets", str(temperature) + ";0")

        time.sleep(1)

    global last_humidifier_status
    if mean_humidity < utils.HUMIDIFIER_LOWER_THRESHOLD and last_humidifier_status != -1:
        last_humidifier_status = 1

        aux_client.publish("henriqueblang/gadgets", "-1;1")

    elif mean_humidity > utils.HUMIDIFIER_UPPER_THRESHOLD and last_humidifier_status != 1:
        last_humidifier_status = -1

        aux_client.publish("henriqueblang/gadgets", "-1;-1")

    last_ac_temperature = ac_temperature

    weather_data.clear()

if __name__ == "__main__":

    client = mqtt.Client("Projeto_2")
    client.connect(utils.TOPIC)

    print("Connected!")

    client.loop_start()

    while True:
        client.subscribe("henriqueblang/weather-data")
        client.on_message = on_message 

    client.loop_stop()