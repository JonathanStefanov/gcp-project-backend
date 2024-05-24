from PIL import Image, ImageDraw, ImageFont
import datetime
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
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")

    with webfont(font_url) as font_stream:

        font = ImageFont.truetype(font_stream, FONT_SIZE)
    with webfont(font_url) as font_stream:

        font_min = ImageFont.truetype(font_stream, FONT_SIZE - 15)
    with webfont(font_url) as font_stream:

        font_big = ImageFont.truetype(font_stream, FONT_SIZE + 15)

    # Text and icon positions
    text_position = (M5STACK_X_SIZE // 2 -FONT_SIZE - 20 , 20)
    date_text_position = (M5STACK_X_SIZE // 2 -FONT_SIZE , 0)
    weather_icon_position = (M5STACK_X_SIZE // 2  - WEATHER_ICON_X_SIZE - 10, 60)
    
    # Draw elements
    draw.text(text_position, current_time, font=font_big, fill='black')
    draw.text(date_text_position, current_date, font=font_min, fill='black')

    icon = fetch_weather_icon(outdoor_weather['current_weather']['icon_url'])
    img.paste(icon, weather_icon_position, icon)

    draw.text((M5STACK_X_SIZE // 2 + 10, 90), f"{outdoor_weather['current_weather']['temperature_c']}°C", font=font, fill='black')
    draw.text((15, 210), f"{indoor_weather['temperature']}°C", font=font_min, fill='black')
    draw.text((M5STACK_X_SIZE // 2 - 25, 210), f"{indoor_weather['humidity']} %", font=font_min, fill='black')
    draw.text((M5STACK_X_SIZE - 75, 210), f"{indoor_weather['co2']} ppm", font=font_min, fill='black')


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