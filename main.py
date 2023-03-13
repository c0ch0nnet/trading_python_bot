
# покупаем, когда позиция = 0. цена покупки - по рынку
# в ином случае, продаем. цена продажи - цена покупки + маржа

last_price = 90
step = 1
buy_price = last_price - step
position_price = buy_price
margin = 5
sell_price = position_price + margin
position_size = 1

if position_size > 0:
    print(f'Продать доллары по {sell_price}')
else:
    print(f'Купить доллары по {buy_price}')