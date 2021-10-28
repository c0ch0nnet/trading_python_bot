import time
import random
import requests


def get_last_price():
    last_price = random.randint(65, 99)
    print(f'Цена последней сделки: {last_price}')
    return last_price

url = "https://test.deribit.com/api/v2/"
headers = {'Content-Type': 'application/json'}

def _auth():
    method = 'public/auth'
    params = {
        'grant_type': 'client_credentials',
        'client_secret': 'CJYqU9lP3NKQ51ToC28rbE9acMOwtkv4h8qaS2KV2dk',
        'client_id': 'aqPeRlFO',
        'scope': 'session:micropython'
    }
    data = {
        'method': method,
        'params': params
    }
    result = requests.post(url=url, headers=headers, json=data).json()['result']
    return result['access_token']

def get_position():
    headers['Authorization'] = 'Bearer {}'.format(_auth())
    data = {
        'method': 'private/get_position',
        'params': {'instrument_name': 'ETH-PERPETUAL'}
    }
    result = requests.post(url=url, headers=headers, json=data).json().get('result')
    position_size = result.get('size')
    position_price = result.get('average_price')
    print(f'Размер позиции: {position_size}')
    print(f'Цена позиции: {position_price}')
    return position_size, position_price

def get_open_order():
    headers['Authorization'] = 'Bearer {}'.format(_auth())
    open_order = random.randint(0, 2)
    print(f'Открытые заявки: {open_order}')
    return open_order

def create_sell_order(sell_price):
    headers['Authorization'] = 'Bearer {}'.format(_auth())
    print(f'Продать доллары по {sell_price}')

def create_buy_order(buy_price):
    headers['Authorization'] = 'Bearer {}'.format(_auth())
    print(f'Купить доллары по {buy_price}')




