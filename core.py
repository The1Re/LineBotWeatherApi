import utm
import numpy as np
import requests

# convert 4 point of UTM to lat and lon
def utmToLatLon(p1: tuple, p2:tuple, p3:tuple, p4:tuple, zone:int = 47) -> tuple:
    x, y = np.mean((p1, p2, p3, p4), axis=0) #find mid point
    
    return utm.to_latlon(x,y, zone_number=zone, zone_letter='N') #return (lat, lon)

def getWeather(lat: float, lon:float, api_key: str) -> dict:
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey={api_key}"
    response = requests.get(url).json()
    values = response['data']['values']

    temp = values['temperature']
    humidity = values['humidity']
    windSpeed = values['windSpeed']
    dewPoint = values['dewPoint']
    rainIntensity = values['rainIntensity']
    
    data = {
        'temp' : temp,
        'humidity' : humidity,
        'windSpeed' : windSpeed,
        'dewPoint' : dewPoint,
        'rainIntensity' : rainIntensity
    }

    return data