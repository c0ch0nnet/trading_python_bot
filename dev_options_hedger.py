import time
import random
from exchanges.deribit import DeribitExchangeInterface
from log import setup_custom_logger

# API_KEY = ""
# API_SECRET = ""
# BASE_URL = "https://www.deribit.com"
# API_URL = "/api/v2/"
# INSRUMENT = 'ETH-PERPETUAL'

dali_tcs = 't.PTbyAbOqAnEhvcJExoHG_tTtQyPBRmdaUHCNMKrqCL5627Wq5GDmJC49dSGRla2gvferzwT8r_QtiOBEG-zzww'
# {
#   "trackingId": "af9ec87804088a71",
#   "payload": {
#     "brokerAccountType": "Tinkoff",
#     "brokerAccountId": "SB18390081"
#   },
#   "status": "Ok"
# }

# curl -X GET "https://api-invest.tinkoff.ru/openapi/sandbox/market/candles?figi=BBG333333333&from=2021-08-18T18%3A38%3A33%2B03%3A00&to=2021-08-19T18%3A38%3A33%2B03%3A00&interval=1min" -H "accept: application/json" -H "Authorization: Bearer t.PTbyAbOqAnEhvcJExoHG_tTtQyPBRmdaUHCNMKrqCL5627Wq5GDmJC49dSGRla2gvferzwT8r_QtiOBEG-zzww"

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

def update_by_positions(calculate_mandatory_size, calculate_optional_size, positions_size):
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
    else:
        optional_size, mandatory_size = 0, 0
    return optional_size, mandatory_size

def create_orders_by_size(current_price, size, mandatory=False):
    if size < 0:
        order = {'price': current_price - 5, 'size': -size, 'side': 'sell'}
    elif size > 0:
        order = {'price': current_price + 5, 'size': size, 'side': 'buy'}
    else:
        order = {}
    if mandatory and 'price' in order.keys():
        order['post_only'] = False
    return order

def create_orders(current_price, optional_size, mandatory_size):
    to_create = []
    to_create_optional = create_orders_by_size(current_price, optional_size)
    to_create_mandatory = create_orders_by_size(current_price, mandatory_size, True)
    if to_create_optional != {}:
        to_create.append(to_create_optional)
    if to_create_mandatory != {}:
        to_create.append(to_create_mandatory)
    return to_create


strike_price = 4150
loop_interval = 10


# for current_price in range(0,1):
# for current_price in range(4030, 4031):
#     current_price = 4003.29
#     positions_size = -1.0
#     calculate_mandatory_size, calculate_optional_size = calculate_grid_positions(strike_price, current_price)
#     optional_size, mandatory_size = update_by_positions(calculate_mandatory_size, calculate_optional_size, positions_size)
#     to_create = create_orders(current_price, optional_size, mandatory_size)
#
#     print(to_create)
#
#     print(f'{current_price:7.0f} '
#           f'{optional_size:7.0f} '
#           f'{mandatory_size:7.0f} '
#           f'{calculate_optional_size:7.0f} '
#           f'{calculate_mandatory_size:7.0f} '
#           f'{calculate_optional_size + calculate_mandatory_size:7.0f} '
#           f'{positions_size:7.0f}')
#     # to_create_optional = {order for order in create_orders(current_price, optional_size) if order.get('price') is not None}
#     print()


# sourse_open_orders = client.get_open_orders()

# open_orders = [{'size': order.get('size'),
#                 'price': order.get('price'),
#                 'side': order.get('side')} for order in client.get_open_orders()]
#
# to_create = [{'size': order.get('size'),
#                'price': order.get('price'),
#                'side': order.get('side')} for order in calc_orders
#              if {'size': order.get('size'),
#                  'price': order.get('price'),
#                  'side': order.get('side')} not in open_orders]
#
# calc_orders = [{'size': order.get('size'),
#                 'price': order.get('price'),
#                 'side': order.get('side')} for order in calc_orders]
# to_cancel = [order.get('order_id') for order in sourse_open_orders
#              if {'size': order.get('size'),
#                  'price': order.get('price'),
#                  'side': order.get('side')} not in calc_orders]

# if len(to_cancel) > 0:
#     logger.info("Canceling %d orders:" % (len(to_cancel)))
#     for order in to_cancel:
#         logger.info(f"  {order}")
#         client.cancel_order(order)

positions = client.get_action_options_strikes()
print(positions)
    # = 'ETH-12NOV21-3900-C'

# while True:
#     try:
#         current_price = client.get_last_trade_price()
#         positions_size = client.get_positions().get('size')
#         client.cancel_all_orders()
#     except Exception as r:
#         logger.info(f'error: {r}')
#
#     calculate_mandatory_size, calculate_optional_size = calculate_grid_positions(strike_price, current_price)
#     optional_size, mandatory_size = update_by_positions(calculate_mandatory_size, calculate_optional_size, positions_size)
#     to_create = create_orders(current_price, optional_size, mandatory_size)
#
#     logger.info(f'current_price: {current_price}')
#     logger.info(f'positions_size: {positions_size}')
#     logger.info(f'strike_price: {strike_price}')
#     logger.info(f'optional_size: {optional_size}')
#     logger.info(f'mandatory_size: {mandatory_size}')
#
#
#     logger.info("calculated orders grid:")
#     for order in to_create:
#         logger.info("  %4s %.2f @ %.4f" % (
#             order.get('side'), order.get('size'), order.get('price')))
#
#     if len(to_create) > 0:
#         logger.info("Creating %d orders:" % (len(to_create)))
#         for order in to_create:
#             try:
#                 responce = client.create_order(order)
#                 logger.info("  %4s %.2f @ %.4f" % (
#                     responce.get('side'), responce.get('size'), responce.get('price')))
#             except Exception as r:
#                 logger.info(f'error: {r}')
#
#     logger.info('====================')
#     time.sleep(loop_interval)
#

