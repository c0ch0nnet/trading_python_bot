import random


def get_last_price():
    last_price = random.randint(65, 99)
    print(f'Цена последней сделки: {last_price}')
    return last_price

def get_position():
    position_size, position_price = random.randint(0, 1), random.randint(65, 99)
    print(f'Размер позиции: {position_size}')
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




