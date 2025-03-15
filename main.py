import time
from deribit import (get_last_price,
                     get_position,
                     get_open_order,
                     create_sell_order,
                     create_buy_order)

step = 1
margin = 100
sleep = 20


def _log_message(message):
    print(message)


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
