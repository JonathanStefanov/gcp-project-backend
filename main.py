from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable to store the last weather data
last_weather_data = None

@app.route('/upload-weather', methods=['POST'])
def upload_weather():
    global last_weather_data
    last_weather_data = request.json
    return jsonify({"status": "success"}), 200

@app.route('/get-weather', methods=['GET'])
def get_weather():
    if last_weather_data is None:
        return jsonify({"error": "No weather data found"}), 404
    return jsonify(last_weather_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
