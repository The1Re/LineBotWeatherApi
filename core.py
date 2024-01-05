import utm
import numpy as np
import requests

def utmToLatLon(p1: tuple, p2:tuple, p3:tuple, p4:tuple, zone:int = 47) -> tuple:
    x, y = np.mean((p1, p2, p3, p4), axis=0) #mid point
    
    return utm.to_latlon(x,y, zone_number=zone, zone_letter='N') #return (lat, lon)

def getWeather(lat: float, lon:float, api_key: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()

    temp = response['main']['temp'] - 273.15
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    
    data = {
        'temp' : temp,
        'pressure' : pressure,
        'humidity' : humidity,
        'wind_speed' : wind_speed
    }

    return data