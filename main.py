from flask import Flask, request, jsonify
import requests
from weather_api import get_outdoor_weather
from auth import token_required
from bigquery_client import insert_weather_data, get_last_weather_data

app = Flask(__name__)


# Variable to store the last weather data
last_weather_data = None

@app.route('/get_outdoor_weather')
@token_required
def outdoor_weather_route():
    return get_outdoor_weather()

@app.route('/upload_indoor_weather', methods=['POST'])
@token_required
def upload_indoor_weather_route():
    # Retrieve data from the POST request
    data = request.get_json()
    
    temperature, humidity, pressure = data.get('temperature'), data.get('humidity'), data.get('pressure')

    # Insert the data into BigQuery
    if insert_weather_data(temperature, pressure, humidity):
        return jsonify({"message": "Data received successfully"})
    else:
        return jsonify({"error": "Failed to insert data into BigQuery"}), 500
    
@app.route('/get_last_indoor_weather')
@token_required
def last_indoor_weather_route():
    return jsonify(get_last_weather_data())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
