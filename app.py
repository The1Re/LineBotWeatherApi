from flask import Flask, jsonify, request, abort
import requests
from dotenv import load_dotenv
import os
import argparse
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, LocationMessageContent
from core import getWeather

load_dotenv()
API_KEY = os.getenv('API_KEY')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_TOKEN = os.getenv('CHANNEL_TOKEN')

app = Flask(__name__)
handle = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_TOKEN)

parser = argparse.ArgumentParser()
parser.add_argument('-d','--debug',help='Debug mode for Developer', action='store_true')
args = parser.parse_args()

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body : " + body)

    try:
        handle.handle(body, signature)
    except InvalidSignatureError :
        app.logger.info('Invalid signature. Please check your Channel Access Token/Channel Secret.')
        abort(400)
    
    return 'OK'

@handle.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event: MessageEvent):
    lat, lon = event.message.latitude, event.message.longitude
    data = getWeather(lat, lon, API_KEY)
    show = (
        "Temperature : {:n} °C\n"
        "Humidity : {} %\n"
        "Wind speed : {} m/s\n"
        "DewPoint : {} °C\n"
        "RainIntensity : {} mm/hr"
    ).format(data['temp'], data['humidity'], data['windSpeed'], data['dewPoint'], data['rainIntensity'])

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[
                    TextMessage(text=f"Address = {event.message.address}"),
                    TextMessage(text=f"lat = {lat:.3f}, lon = {lon:.3f}"),
                    TextMessage(text=show)
                ]
            )
        )

if __name__ == '__main__':
    app.run(debug= args.debug)