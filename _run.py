from _d_api import *
import time

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
