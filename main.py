import re
import os
import json
import requests
from flask import Flask, request, jsonify
from flask_sslify import SSLify

app = Flask(__name__)
sslify = SSLify(app)

TOKEN = os.environ['TOKEN']
API_URL = f'https://api.telegram.org/bot{TOKEN}/'

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    r = request.get_json()

    message = r['message']
    chat_id = message['chat']['id']
    message_text = message['text']
    send_message(chat_id, get_price(parse_text(message_text)))

    return jsonify(r)

  return '<h1>One chance to change everything</h1>'

def parse_text(text):
  currency = re.search(r'/\w+', text)

  if currency:
    return currency.group()[1:]

  return text

def get_price(currency):
  if currency == None:
    return None

  try:
    r = requests.get(f'https://api.coinmarketcap.com/v1/ticker/{currency}').json()
    price = r[-1]['price_usd']
    return f'{price} usd'
  except Exception as e:
    return currency

def send_message(chat_id, message='How much is /bitcoin today?'):
  url = API_URL + 'sendMessage'
  body = {
    'chat_id': chat_id,
    'text': message
  }
  return requests.post(url, json=body)

def main():
  app.run()

if __name__ == '__main__':
  main()
