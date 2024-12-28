import os

import requests
from dotenv import load_dotenv

load_dotenv()

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
access_token = _auth(base_url)

balance = get_balance(base_url, access_token)
print(f'Баланс счета составляет {balance} BTC')
