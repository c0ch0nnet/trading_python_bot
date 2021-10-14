import random
import time

def get_last_price():
    last_price = random.randint(65, 99)
    print(f'Цена последней сделки: {last_price}')
    return last_price

def get_position():
    position_size, position_price = random.randint(0, 1), random.randint(65, 99)
    print(f'Размер позиции: {last_price}')
    print(f'Цена позиции: {position_price}')
    return position_size, position_price

def get_open_order():
    open_order = random.randint(0, 2)
    print(f'Открытые заявки: {open_order}')
    return open_order

def create_sell_order(sell_price):
    print(f'Продать доллары по {sell_price}')

def create_buy_order(buy_price):
    print(f'Купить доллары по {buy_price}')


step = 1
margin = 5
loop_interval = 10

while True:
    last_price = get_last_price()
    position_size, position_price = get_position()
    open_order = get_open_order()

    buy_price = last_price - step
    sell_price = position_price + margin

    if position_size > 0 and open_order == 0:
        create_sell_order(sell_price)
    elif open_order == 0:
        create_buy_order(buy_price)
    else:
        print(f'Ничего не делаем')

    print('====================')
    time.sleep(loop_interval)
