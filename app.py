from flask import Flask, request, jsonify, send_file
import requests
import signal
from types import FrameType
from weather_api import get_outdoor_weather
from auth import token_required
from bigquery_client import insert_weather_data, get_last_weather_data, get_current_user_name, update_current_user_name, get_mean_weather_data_per_hour
from utils.logging import logger
from utils.logging import flush
import sys 
from image_generator import generate_image
from text_to_speech import generate_tts
from health import health_status
app = Flask(__name__)



@app.route('/get_outdoor_weather')
@token_required
def outdoor_weather_route():
    return jsonify(get_outdoor_weather())

@app.route('/upload_indoor_weather', methods=['POST'])
@token_required
def upload_indoor_weather_route():
    # Retrieve data from the POST request
    data = request.get_json()
    
    temperature, humidity, pressure, co2 = data.get('temperature'), data.get('humidity'), data.get('pressure'), data.get('co2')

    # Insert the data into BigQuery
    if insert_weather_data(temperature, pressure, humidity, co2):
        return jsonify({"message": "Data received successfully"})
    else:
        return jsonify({"error": "Failed to insert data into BigQuery"}), 500
    
@app.route('/get_last_indoor_weather')
@token_required
def last_indoor_weather_route():
    return jsonify(get_last_weather_data())

@app.route('/get_mean_indoor_weather')
@token_required
def mean_indoor_weather_route():
    return jsonify(get_mean_weather_data_per_hour())


@app.route('/generate_image')
@token_required
def generate_image_route():
    img = generate_image()
    img.save("output.png")
    return send_file('output.png', mimetype='image/png')

@app.route('/generate_tts')
@token_required
def generate_tts_route():
    data = "Outside: " + str(get_outdoor_weather()) + "Inside: " + str(get_last_weather_data())
    generate_tts(data)
    return send_file('output.wav', mimetype='audio/mpeg'), 200



@app.route('/get_current_user_name')
@token_required
def get_current_user_name_route():
    return jsonify({"name" : get_current_user_name()})

@app.route('/update_current_user_name', methods=['POST'])
@token_required
def update_current_user_name_route():
    data = request.get_json()
    new_name = data.get('name')
    update_current_user_name(new_name)
    return jsonify({"message": "Data received successfully"})

@app.route('/health')
@token_required
def health():
    return jsonify(health_status())

def shutdown_handler(signal_int: int, frame: FrameType) -> None:
    logger.info(f"Caught Signal {signal.strsignal(signal_int)}")


    flush()

    # Safely exit program
    sys.exit(0)

if __name__ == "__main__":
    # Running application locally, outside of a Google Cloud Environment

    # handles Ctrl-C termination
    signal.signal(signal.SIGINT, shutdown_handler)

    app.run(host="localhost", port=8080, debug=True)
else:
    # handles Cloud Run container termination
    signal.signal(signal.SIGTERM, shutdown_handler)
