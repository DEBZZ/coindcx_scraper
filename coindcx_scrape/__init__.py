import requests
from dotenv import load_dotenv
import os
import hmac
import hashlib
import base64
import json
import time
import requests
from coindcx_scrape.market_data import fetch_market_data
import jsonify


load_dotenv()
dict_apis = {
    "trade_history": "https://api.coindcx.com/exchange/v1/orders/trade_history",
    "new_order": "https://api.coindcx.com/exchange/v1/orders/create",
    "account_balance": "https://api.coindcx.com/exchange/v1/users/balances",
    "market": "https://api.coindcx.com/exchange/ticker"
}

key = os.getenv("key")
secret = os.getenv("secret_key")

secret_bytes = bytes(secret, encoding='utf-8')

# Generating a timestamp
timeStamp = int(round(time.time() * 1000))

body = {
    "timestamp": timeStamp
}

json_body = json.dumps(body, separators=(',', ':'))

signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

url = dict_apis["trade_history"]

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

response = requests.post(url, data=json_body, headers=headers)
data = response.json()
print(data)

# url = dict_apis["market"]
#
# response = requests.get(url)
# data = response.json()
# print(data[0])
# dict_pos_change = {dt['market']: dt['change_24_hour'] for dt in data if 'change_24_hour' in dt.keys() if
#                    float(dt['change_24_hour']) > 10}
# dict_market = {dt['market']: dt['last_price'] for dt in data if dt['market'] in dict_crypto_purchased.keys()}
# print(dict_pos_change)
