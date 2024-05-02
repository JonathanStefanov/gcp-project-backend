from bigquery_client import get_last_ping_time
from datetime import datetime, timezone
from weather_api import get_outdoor_weather


def check_weatherapi():
    weather_check = get_outdoor_weather()

    return weather_check.get('success', True)


def health_status():
    last_ping = get_last_ping_time()
    current_time = datetime.now(timezone.utc)

    # Calculate the time difference
    time_difference = current_time - last_ping

    minutes = time_difference.total_seconds() // 60

    weatherapi_status = check_weatherapi()

    return {
        "status": "OK",
        "last_ping": str(last_ping),
        "time_difference": f"{minutes} minutes",
        "weatherapi_status": "OK" if weatherapi_status else "DOWN"
    }