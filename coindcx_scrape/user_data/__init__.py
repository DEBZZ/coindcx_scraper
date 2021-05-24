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
dict_account_apis = {
    "trade_history": "https://api.coindcx.com/exchange/v1/orders/trade_history",
    "new_order": "https://api.coindcx.com/exchange/v1/orders/create",
    "account_balance": "https://api.coindcx.com/exchange/v1/users/balances"
}


def fetch_trade_history():
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

    url = dict_account_apis["trade_history"]

    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }

    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    return data
    # dict_crypto_purchased = {dt['symbol']: dt['price'] for dt in data}


def compare():
    data_trade_history = fetch_trade_history()
    dict_crypto_purchased = {dt['symbol']: dt['price'] for dt in data_trade_history}

    data_market_current = fetch_market_data()
    dict_market = {dt['market']: dt['last_price'] for dt in data_market_current if dt['market'] in dict_crypto_purchased.keys() and dt['last_price']<dict_crypto_purchased[dt['market']]}
    print(dict_market)

if __name__ == "__main__":
    compare()



