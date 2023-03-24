
# покупаем, когда позиция = 0. цена покупки - по рынку
# в ином случае, продаем. цена продажи - цена покупки + маржа
import random
import time


def get_last_price():
    return random.randint(69, 90)

def get_position():
    return random.randint(0, 1), random.randint(69, 90)

def get_open_order():
    return random.randint(0, 2)

while True:
    time.sleep(15)
    open_order = get_open_order()
    last_price = get_last_price()
    step = 1
    buy_price = last_price - step
    position_size, position_price = get_position()
    margin = 5
    sell_price = position_price + margin

    print(f'Позиция: {position_price}@{position_size}. Цена последней сделки: {last_price}. '
          f'Количество открытых ордеров = {open_order}')
    if open_order > 0:
        print(f'Уже есть открытые ордера')
        continue
    if position_size > 0:
        print(f'Продать доллары по {sell_price}')
    else:
        print(f'Купить доллары по {buy_price}')
