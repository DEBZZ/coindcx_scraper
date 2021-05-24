import requests

dict_market_apis = {
    "market": "https://api.coindcx.com/exchange/ticker"
}


def fetch_market_data(crypto_currency=None):
    url = dict_market_apis["market"]

    response = requests.get(url)
    data = response.json()
    if crypto_currency :
        return [dt for dt in data if dt['market'] == crypto_currency]
    return data


def fetch_crypto_with_positive_change(percentage_of_change=0):
    data = fetch_market_data()
    dict_pos_change = {dt['market']: dt['change_24_hour'] for dt in data if 'change_24_hour' in dt.keys() if
                       float(dt['change_24_hour']) > percentage_of_change}
    return dict_pos_change
