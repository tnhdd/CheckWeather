import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GEOCODING_API_KEY = os.getenv("GEOCODING_API_KEY")


def get_coordinates(city, country_code):
    city_api_url = 'https://api.api-ninjas.com/v1/geocoding?city={}'.format(city)
    cities_response = requests.get(city_api_url, headers={'X-Api-Key': GEOCODING_API_KEY})
    cities_data = cities_response.json()

    state = None
    if country_code == "US":
        state = input("What is the state? ").title()

    for city_info in cities_data:
        country = city_info.get("country", "Unknow")
        if country == country_code:
            if country == "US":
                if city_info.get("state", "Unknow") == state:
                    return round(city_info.get("latitude"), 2), round(city_info.get("longitude"), 2)
            else:
                return round(city_info.get("latitude"), 2), round(city_info.get("longitude"), 2)

    return None, None


def get_weather():
    city = input("Type the name of the city ")
    country_code = input("Type in country code ").upper()
    lat, lon = get_coordinates(city, country_code)

    if lat and lon:
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(weather_url).json()
        temp = response["main"]["temp"]
        temp_max = response['main']["temp_max"]
        temp_min = response['main']["temp_min"]
        feels_like = response["main"]["feels_like"]
        description = response["weather"][0]["description"]

        print(f"Description: {description}")
        print(f"Feels like: {feels_like}°C")
        print(f"Temperature: {temp}°C")
        print(f"Min temperature: {temp_min}°C")
        print(f"Max temperature: {temp_max}°C")

    else:
        print("City not found.")


get_weather()
