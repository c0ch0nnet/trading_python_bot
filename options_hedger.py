import time
import random
from exchanges.deribit import DeribitExchangeInterface
from log import setup_custom_logger

# API_KEY = ""
# API_SECRET = ""
# BASE_URL = "https://www.deribit.com"
# API_URL = "/api/v2/"
# INSRUMENT = 'ETH-PERPETUAL'

API_KEY = "aqPeRlFO"
API_SECRET = "CJYqU9lP3NKQ51ToC28rbE9acMOwtkv4h8qaS2KV2dk"
BASE_URL = "https://test.deribit.com"
API_URL = "/api/v2/"
INSRUMENT = 'ETH-PERPETUAL'

logger = setup_custom_logger(f'orders_manager.{API_KEY}')

client = DeribitExchangeInterface(API_KEY, API_SECRET, BASE_URL, API_URL, INSRUMENT)



def calculate_grid_positions(strike_price, current_price):
    delta_grid = 50
    start_grid = strike_price - delta_grid + 5
    end_grid = strike_price + delta_grid + 5
    prices = [i for i in range(start_grid, end_grid, 10)]
    if current_price < min(prices):
        return 0, 0
    elif current_price >= max(prices):
        return sum(map(lambda x: x * 0.1, prices)), 0
    else:
        index_price = current_price - 5 if current_price % 10 < 5 else current_price
        index = prices.index(index_price // 5 * 5)
        mandatory_size = sum(map(lambda x: (x) * 0.1, prices[:index]))
        mandatory_size = mandatory_size if mandatory_size % 1 == 0 else mandatory_size + 0.5
        optional_size = sum(map(lambda x: (x) * 0.1, prices[:index+1]))
        optional_size = optional_size if optional_size % 1 == 0 else optional_size + 0.5
        return mandatory_size, optional_size - mandatory_size


# def calculate_orders_grid(strike_price, current_price):
#     delta_grid = 50
#     start_grid = strike_price - delta_grid
#     end_grid = strike_price + delta_grid
#     prices = [i for i in range(start_grid, end_grid, 10)]
#     if current_price < min(prices):
#         positions_mask = [1 for _ in range(10)]
#     elif current_price > max(prices):
#         positions_mask = [-1 for _ in range(10)]
#     else:
#         index = prices.index(current_price // 10 * 10) + 1
#         positions_mask = [-1 for _ in range(index)] + [1 for _ in range(10 - index)]
#     return list(map(lambda m, p: m * p, positions_mask, prices))
#
# def replace_orders_size(source_orders, delta_size):
#     orders = []
#     for order in source_orders:
#         if delta_size >= order.get('size'):
#             delta_size -= order.get('size')
#         elif delta_size < order.get('size'):
#             order['size'] -= delta_size
#             orders.append(order)
#             delta_size = 0
#     return orders

# def get_current_price():
#     return random.randint(3950, 3971)
#
# def get_positions_size():
#     return random.randint(0, 10) * 0.01

strike_price = 4000
loop_interval = 10


for current_price in range(3945, 4055):
    positions_size = 1190 + 398 - 1
    calculate_mandatory_size, calculate_optional_size = calculate_grid_positions(strike_price, current_price)

    optional_size, mandatory_size = 0, 0

    if positions_size < calculate_mandatory_size + calculate_optional_size:
        mandatory_size = calculate_mandatory_size - positions_size
        if mandatory_size < 0:
            optional_size = calculate_optional_size + mandatory_size
            mandatory_size = 0
        else:
            optional_size = calculate_optional_size
    elif positions_size > calculate_mandatory_size + calculate_optional_size:
        mandatory_size = calculate_mandatory_size + calculate_optional_size - positions_size
        if mandatory_size > 0:
            mandatory_size = 0
            optional_size = calculate_optional_size - mandatory_size - positions_size
        else:
            optional_size = 0

    print(f'{current_price:7.0f} '
          f'{optional_size:7.0f} '
          f'{mandatory_size:7.0f} '
          f'{calculate_optional_size:7.0f} '
          f'{calculate_mandatory_size:7.0f} '
          f'{calculate_optional_size + calculate_mandatory_size:7.0f} '
          f'{positions_size:7.0f}')



# while True:
#     current_price = client.get_last_trade_price()
#     logger.info(f'current_price: {current_price}')
#     positions_size = get_positions_size()
#     # client.cancel_all_orders()
#
#     grid_prices = calculate_orders_grid(strike_price, current_price)
#     grid_position = len([order for order in grid_prices if order < 0])
#     orders_sell = [{'price': -price, 'size': -price * 0.1, 'side': 'sell'} for price in grid_prices[:grid_position]]
#     orders_buy = [{'price': price, 'size': price * 0.1, 'side': 'buy'} for price in grid_prices[grid_position:]]
#
#     grid_position_size = sum([order.get('size') for order in orders_sell])
#     position = client.get_positions().get('size')
#     position_size = client.get_positions().get('size')
#
#     delta_size = grid_position_size - position_size
#     # if len(orders_buy) > 0:
#     #     logger.info(replace_orders_size(orders_buy, -delta_size))
#     #     orders_buy = replace_orders_size(orders_buy, -delta_size)
#     # if len(orders_sell) > 0:
#     #     logger.info(replace_orders_size(orders_buy, delta_size))
#     #     orders_sell = replace_orders_size(orders_sell, delta_size)
#
#     orders_buy = replace_orders_size(orders_buy, -delta_size)
#     orders_sell = replace_orders_size(orders_sell, delta_size)
#
#     logger.info("calculated orders grid:")
#     for order in orders_sell + orders_buy:
#         logger.info("  %4s %.2f @ %.4f" % (
#             order.get('side'), order.get('size'), order.get('price')))
#
#     calc_orders = orders_sell + orders_buy
#     sourse_open_orders = client.get_open_orders()
#
#     open_orders = [{'size': order.get('size'),
#                     'price': order.get('price'),
#                     'side': order.get('side')} for order in client.get_open_orders()]
#
#     to_create = [{'size': order.get('size'),
#                    'price': order.get('price'),
#                    'side': order.get('side')} for order in calc_orders
#                  if {'size': order.get('size'),
#                      'price': order.get('price'),
#                      'side': order.get('side')} not in open_orders]
#
#     calc_orders = [{'size': order.get('size'),
#                     'price': order.get('price'),
#                     'side': order.get('side')} for order in calc_orders]
#     to_cancel = [order.get('order_id') for order in sourse_open_orders
#                  if {'size': order.get('size'),
#                      'price': order.get('price'),
#                      'side': order.get('side')} not in calc_orders]
#
#     if len(to_cancel) > 0:
#         logger.info("Canceling %d orders:" % (len(to_cancel)))
#         for order in to_cancel:
#             logger.info(f"  {order}")
#             client.cancel_order(order)
#
#     if len(to_create) > 0:
#         logger.info("Creating %d orders:" % (len(to_create)))
#         for order in to_create:
#             responce = client.create_order(order)
#             logger.info("  %4s %.2f @ %.4f" % (
#                 responce.get('side'), responce.get('size'), responce.get('price')))
#
#     logger.info('====================')
#     time.sleep(loop_interval)

