import requests
from flask import jsonify
import os
from dotenv import load_dotenv

load_dotenv()
WEATHER_API = os.getenv('WEATHER_API')
WEATHER_URL = "http://api.weatherapi.com/v1/current.json"

def get_outdoor_weather():
    params = {
        "key": WEATHER_API,
        "q": "Lausanne",
        "aqi": "no"
    }
    response = requests.get(WEATHER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature_c": data['current']['temp_c'],
            "condition_text": data['current']['condition']['text'],
            "icon_url": "https:" + data['current']['condition']['icon']
        }
        return jsonify(weather)
    else:
        return jsonify({"error": "Failed to fetch weather data"}), response.status_code