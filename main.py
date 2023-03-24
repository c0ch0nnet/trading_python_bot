import random
import time


def get_last_price():
    return random.randint(69, 90)


def get_position():
    return random.randint(0, 1), random.randint(69, 90)


def get_open_order():
    return random.randint(0, 2)


def create_sell_order(price):
    print(f'Продать доллары по {price}')


def create_buy_order(price):
    print(f'Купить доллары по {price}')


def _log_message(message):
    print(message)


step = 1
margin = 5
sleep = 15

while True:
    time.sleep(sleep)
    open_order = get_open_order()
    last_price = get_last_price()
    buy_price = last_price - step
    position_size, position_price = get_position()
    sell_price = position_price + margin

    _log_message(f'Позиция: {position_price}@{position_size}. Цена последней сделки: {last_price}. '
                 f'Количество открытых ордеров = {open_order}')
    if open_order > 0:
        _log_message('Уже есть открытые ордера')
        continue
    if position_size > 0:
        create_sell_order(sell_price)
    else:
        create_buy_order(buy_price)
