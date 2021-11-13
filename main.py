import requests

# покупаем, когда позиция = 0. цена покупки - по рынку
# в ином случае, продаем. цена продажи - цена покупки + маржа

def get_position():
    return 0, 50


brokerAccountId = "SB1495943"
instrument = "BBG004730RP0" # GAZP
token = "t.260pfPA1fw-f0F5SfMFtLiFH5JNjJTvyz6C6-EfFFlHHwc_mSOyDHnbetGsj14vB5yX-CCp79ojX7lyGJThsbg"
position_size, position_price = get_position()

url = f"https://api-invest.tinkoff.ru/openapi/sandbox/orders/limit-order?figi={instrument}&brokerAccountId={brokerAccountId}"
headers = {"Authorization": f"Bearer {token}"}


print(url, headers)
if position_size == 0:
    print("покупаем")
else:
    print("продаем")