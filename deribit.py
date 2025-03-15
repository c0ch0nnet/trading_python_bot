import os

import requests
from dotenv import load_dotenv

load_dotenv()


def get_last_price():
    access_token = _auth(base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    method = 'public/get_last_trades_by_instrument'
    params = {'instrument_name': os.getenv('INSTRUMENT'), 'count': 1}

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result')
    return result['trades'][0]['price'] if result else None


def get_position():
    access_token = _auth(base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    method = 'private/get_position'
    params = {'instrument_name': os.getenv('INSTRUMENT')}

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result')
    return result.get('size', 0), result.get('average_price')


def get_open_order():
    access_token = _auth(base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    method = 'private/get_open_orders_by_instrument'
    params = {'instrument_name': os.getenv('INSTRUMENT')}

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result')
    size = 0 if len(result) == 0 else result[0].get('amount')
    return size


def create_sell_order(price):
    access_token = _auth(base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    method = 'private/sell'
    params = {
        'instrument_name': os.getenv('INSTRUMENT'),
        'amount': 10,
        'price': price,
        'post_only': 'true',
        'time_in_force': 'good_til_cancelled',
        'type': 'limit',
    }

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result', {}).get('order', {})

    print(f'Продать биткойны по {result.get("price")}')


def create_buy_order(price):
    access_token = _auth(base_url)
    headers = {'Authorization': f'Bearer {access_token}'}
    method = 'private/buy'
    params = {
        'instrument_name': os.getenv('INSTRUMENT'),
        'amount': 10,
        'price': price,
        # 'post_only': 'true',
        'time_in_force': 'good_til_cancelled',
        'type': 'limit',
    }

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result', {}).get('order', {})

    print(f'Купить биткойны по {result.get("price")}')


def _auth(base_url):
    method = 'public/auth'
    params = {
        'grant_type': 'client_credentials',
        'client_secret': os.getenv('CLIENT_SECRET'),
        'client_id': os.getenv('CLIENT_ID'),
    }
    response = requests.get(f'{base_url}{method}', params=params)
    result = response.json().get('result')
    access_token = result.get('access_token')
    return access_token

def get_balance(base_url, access_token):
    method = 'private/simulate_portfolio'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'currency': 'BTC'}

    response = requests.get(f'{base_url}{method}', params=params, headers=headers)
    result = response.json().get('result')
    balance = result.get('balance')
    return balance

base_url = 'https://test.deribit.com/api/v2/'
# access_token = _auth(base_url)

# balance = get_balance(base_url, access_token)
# print(f'Баланс счета составляет {balance} BTC')
