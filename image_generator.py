from PIL import Image, ImageDraw, ImageFont
import datetime
from datetime import timedelta
import requests
from io import BytesIO
import urllib.request
import functools
import io
from weather_api import get_outdoor_weather
from bigquery_client import get_last_weather_data

# Constants
M5STACK_X_SIZE = 320
M5STACK_Y_SIZE = 240
WEATHER_ICON_X_SIZE = 100
WEATHER_ICON_Y_SIZE = 100
FONT_SIZE = 30

def fetch_weather_icon(icon_url):
    response = requests.get(icon_url)
    icon = Image.open(BytesIO(response.content))
    icon = icon.resize((WEATHER_ICON_X_SIZE, WEATHER_ICON_Y_SIZE))
    return icon.convert("RGBA")

def fetch_forecast_weather_icon(icon_url):
    response = requests.get(icon_url)
    icon = Image.open(BytesIO(response.content))
    icon = icon.resize((50, 50))
    return icon.convert("RGBA")

@functools.lru_cache
def get_font_from_url(font_url):
    return urllib.request.urlopen(font_url).read()

def webfont(font_url):
    return io.BytesIO(get_font_from_url(font_url))

def create_base_image():
    # Load the background image from a file
    img = Image.open('assets/bg1.png')
    
    # Optionally resize the image if it's not the correct dimensions
    if img.size != (M5STACK_X_SIZE, M5STACK_Y_SIZE):
        img = img.resize((M5STACK_X_SIZE, M5STACK_Y_SIZE))
    
    return img.convert("RGBA")


def draw_weather(img, font_url, outdoor_weather, indoor_weather):
    draw = ImageDraw.Draw(img)
    now = datetime.datetime.now() + timedelta(hours=2)
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")

    with webfont(font_url) as font_stream:

        font = ImageFont.truetype(font_stream, FONT_SIZE)
    with webfont(font_url) as font_stream:

        font_min = ImageFont.truetype(font_stream, FONT_SIZE - 15)
    with webfont(font_url) as font_stream:

        font_big = ImageFont.truetype(font_stream, FONT_SIZE + 15)
    with webfont(font_url) as font_stream:

        font_smallest = ImageFont.truetype(font_stream, FONT_SIZE - 20)


    # Text and icon positions
    text_position = (M5STACK_X_SIZE // 2 -FONT_SIZE - 20 , 10)
    date_text_position = (M5STACK_X_SIZE // 2 -FONT_SIZE , 0)
    weather_icon_position = (M5STACK_X_SIZE // 2  - WEATHER_ICON_X_SIZE - 10, 35)
    
    # Draw elements
    draw.text(text_position, current_time, font=font_big, fill='black')
    draw.text(date_text_position, current_date, font=font_min, fill='black')

    icon = fetch_weather_icon(outdoor_weather['current_weather']['icon_url'])
    img.paste(icon, weather_icon_position, icon)

    draw.text((M5STACK_X_SIZE // 2 + 10, 65), f"{outdoor_weather['current_weather']['temperature_c']}°C", font=font, fill='black')
    draw.text((15, 222), f"{indoor_weather['temperature']}°C", font=font_min, fill='black')
    draw.text((M5STACK_X_SIZE // 2 - 25, 222), f"{indoor_weather['humidity']} %", font=font_min, fill='black')
    draw.text((M5STACK_X_SIZE - 75, 222), f"{indoor_weather['co2']} ppm", font=font_min, fill='black')

    # Forecast
    forecast = outdoor_weather['forecast']
    for i, day in enumerate(forecast):
        icon = fetch_forecast_weather_icon(day['icon_url'])
        img.paste(icon, (25 + i * 110, 110), icon)

        # Calculate the future date for each forecasted day
        future_date = now + timedelta(days=i)
        date_str = future_date.strftime("%d/%m")  # Format the date as day/month for display

        # Draw the temperature forecast and the future date
        draw.text((20 + i * 110, 165), f"{day['min_temp']}°C/{day['max_temp']}°C", font=font_smallest, fill='black')
        draw.text((35 + i * 110, 155), date_str, font=font_smallest, fill='black')


    return img

def generate_image():
    # Fetch weather data
    outdoor_weather = get_outdoor_weather()
    indoor_weather = get_last_weather_data()

    # Define the font URL
    font_url = "https://github.com/google/fonts/raw/main/ufl/ubuntu/Ubuntu-Regular.ttf"

    # Create base image and draw weather
    img = create_base_image()
    final_image = draw_weather(img, font_url, outdoor_weather, indoor_weather)

    # Save or show image
    final_image.save("digital_thermometer.png")
    return final_image

if __name__ == "__main__":
    generate_image()
    print("Image generated successfully")