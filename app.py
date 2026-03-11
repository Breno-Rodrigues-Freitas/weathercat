import streamlit as st
import requests
import os
from dotenv import load_dotenv
from cat_engine import choose_cat

load_dotenv()

API_KEY = os.getenv("API_KEY")

st.title("🐱 WeatherCat")
st.write("Weather and cat mood based on your city")

city = st.text_input("Enter a city")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None


if city:

    data = get_weather(city)

    if data:

        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        cat = choose_cat(temperature, weather)

        st.subheader(f"Weather in {city}")
        st.write(f"Temperature: {temperature} °C")
        st.write(f"Condition: {weather}")
        st.write(f"Humidity: {humidity}%")

        st.subheader("Cat mood")
        st.write(cat)

    else:
        st.write("City not found.")
