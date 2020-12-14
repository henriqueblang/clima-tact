import json
import requests
import paho.mqtt.client as mqtt
import time

import utils

def get_weather_data():
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    querystring = {"q":"Santa Rita do Sapucai,mg,br","lat":"-22.2457125","lon":"-45.7097005","callback":"test","id":"2172797","lang":"null","units":"\"metric\" or \"imperial\"","mode":"xml, html"}

    headers = {
        'x-rapidapi-key': "f662b8d173mshbdbfffcde621ff3p129e30jsn74e6d62a0bdf",
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    clear_response = response.text.replace('test(','').replace(')','')
    resp_json = json.loads(clear_response)

    humidity = resp_json['main']['humidity']
    
    t_kelvin = resp_json['main']['temp']
    t_celsius = t_kelvin - 273.15

    return humidity, round(t_celsius, 2)

if __name__ == "__main__":

    client = mqtt.Client("Projeto_1")
    client.connect(utils.TOPIC)

    print("Connected!")
    
    while True:
        humidity, temperature = get_weather_data()

        print(f"[crawler] Sent humity: {humidity}, temperature: {temperature}")

        client.publish("henriqueblang/weather-data", str(humidity) + ";" + str(temperature))

        time.sleep(utils.DATA_PUBLISH_INTERVAL)