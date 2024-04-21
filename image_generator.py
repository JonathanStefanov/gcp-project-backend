# Adjusting the code with a larger font size for the time

from PIL import Image, ImageDraw, ImageFont
import datetime

# Create a new image with white background
img = Image.new('RGB', (320, 240), color='white')
d = ImageDraw.Draw(img)

# Define fonts with increased size for time
try:
    font_time = ImageFont.truetype("arial.ttf", 40)  # Increased size for time
    font_data = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font_time = ImageFont.load_default()
    font_data = ImageFont.load_default()

# Display current time centered and larger at the top
current_time = datetime.datetime.now().strftime("%H:%M")
time_bbox = d.textbbox((0, 0), current_time, font=font_time)
time_width = time_bbox[2] - time_bbox[0]
time_x = (320 - time_width) // 2
d.text((time_x, 10), current_time, font=font_time, fill=(0, 0, 0))

# Data to display in the quadrant, except weather description
data = {
    "Temperature Indoor": "22°C",
    "Humidity Indoor": "45%",
    "Pressure Indoor": "1012 hPa",
    "CO2 Indoor": "900 ppm",
    "Temperature Outdoor": "18°C",
    "Wind Speed": "5 km/h"
}

# Calculate the quadrant positions and dimensions
start_x, start_y = 10, 80  # Adjusted Y start for more space due to bigger time font
col_width = 150
row_height = 30

for i, (key, value) in enumerate(data.items()):
    x = start_x + (i % 2) * col_width
    y = start_y + (i // 2) * row_height
    d.text((x, y), f"{key}: {value}", font=font_data, fill=(0, 0, 0))

# Save and display the image
img_path = "digital_thermometer.png"
img.save(img_path)
img.show()

img_path
