from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
import os
import argparse

app = Flask(__name__)

load_dotenv()
api_key = os.getenv('API_KEY')

parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug',help='Debug mode for Deverlop', action='store_true')
args = parser.parse_args()

@app.route('/', methods=['GET'])
def index():
    lat, lon = 12.646, 101.171
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()

    temp = response['main']['temp'] - 273
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    
    data = {
        'temp' : temp,
        'pressure' : pressure,
        'humidity' : humidity,
        'wind_speed' : wind_speed
    }

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug= args.debug)