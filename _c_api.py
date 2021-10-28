import time
import random
import requests


class Deribit():

    def __init__(self, key, secret, url, instrument):
        self.url = url
        self.instrument = instrument
        self.key = key
        self.secret = secret
        self.headers = {'Content-Type': 'application/json'}

    def _auth(self):
        method = 'public/auth'
        params = {
            'grant_type': 'client_credentials',
            'client_secret': self.secret,
            'client_id': self.key,
            'scope': 'session:micropython'
        }
        data = {
            'method': method,
            'params': params
        }
        result = requests.post(url=self.url, headers=self.headers, json=data).json().get('result')
        return result['access_token']

    def get_position(self):
        self.headers['Authorization'] = 'Bearer {}'.format(self._auth())
        data = {
            'method': 'private/get_position',
            'params': {'instrument_name': self.instrument}
        }
        result = requests.post(url=self.url, headers=self.headers, json=data).json().get('result')
        position_size = result.get('size')
        position_price = result.get('average_price')
        print(f'Размер позиции: {position_size}')
        print(f'Цена позиции: {position_price}')
        return position_size, position_price


def get_last_price():
    last_price = random.randint(65, 99)
    print(f'Цена последней сделки: {last_price}')
    return last_price

# def get_position():
#     position_size, position_price = random.randint(0, 1), random.randint(65, 99)
#     print(f'Размер позиции: {position_size}')
#     print(f'Цена позиции: {position_price}')
#     return position_size, position_price

def get_open_order():
    open_order = random.randint(0, 2)
    print(f'Открытые заявки: {open_order}')
    return open_order

def create_sell_order(sell_price):
    print(f'Продать доллары по {sell_price}')

def create_buy_order(buy_price):
    print(f'Купить доллары по {buy_price}')




