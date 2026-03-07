import requests
import os
from dotenv import load_dotenv
from cat_engine import choose_cat

load_dotenv()

API_KEY=os.getenv("API_KEY")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


city = input("Enter the city name: ")

data = get_weather(city)

if data:

    temperature = data["main"]["temp"]
    weather = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]

    cat = choose_cat(temperature, weather)

    print(f"\nWeather in {city}")
    print(f"Temperature: {temperature}°C")
    print(f"Condition: {weather}")
    print(f"Humidity: {humidity}%")
    print(f"Cat mood: {cat}")

else:
    print("Error fetching weather data.")