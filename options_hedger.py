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

def calculate_orders_grid(strike_price, current_price):
    delta_grid = 50
    start_grid = strike_price - delta_grid
    end_grid = strike_price + delta_grid
    prices = [i for i in range(start_grid, end_grid, 10)]
    if current_price < min(prices):
        positions_mask = [-1 for _ in range(10)]
    elif current_price > max(prices):
        positions_mask = [1 for _ in range(10)]
    else:
        index = prices.index(current_price // 10 * 10) + 1
        positions_mask = [1 for _ in range(index)] + [-1 for _ in range(10 - index)]
    return list(map(lambda m, p: m * p, positions_mask, prices))

def replace_orders_size(source_orders, delta_size):
    orders = []
    for order in source_orders:
        if delta_size >= order.get('size'):
            delta_size -= order.get('size')
        elif delta_size < order.get('size'):
            order['size'] -= delta_size
            orders.append(order)
            delta_size = 0
    return orders

def get_current_price():
    return random.randint(3950, 4050)

def get_positions_size():
    return random.randint(0, 10) * 0.01

strike_price = 4050
loop_interval = 10


while True:
    current_price = client.get_last_trade_price() - 1
    logger.info(f'current_price: {current_price}')
    positions_size = get_positions_size()
    # client.cancel_all_orders()

    grid_prices = calculate_orders_grid(strike_price, current_price)
    grid_position = len([order for order in grid_prices if order < 0])
    orders_sell = [{'price': -price, 'size': -price * 0.1, 'side': 'sell'} for price in grid_prices[:grid_position]]
    orders_buy = [{'price': price, 'size': price * 0.1, 'side': 'buy'} for price in grid_prices[grid_position:]]

    grid_position_size = sum([order.get('size') for order in orders_sell])
    position = client.get_positions().get('size')
    position_size = client.get_positions().get('size')

    delta_size = grid_position_size - position_size
    # if len(orders_buy) > 0:
    #     logger.info(replace_orders_size(orders_buy, -delta_size))
    #     orders_buy = replace_orders_size(orders_buy, -delta_size)
    # if len(orders_sell) > 0:
    #     logger.info(replace_orders_size(orders_buy, delta_size))
    #     orders_sell = replace_orders_size(orders_sell, delta_size)

    orders_buy = replace_orders_size(orders_buy, -delta_size)
    orders_sell = replace_orders_size(orders_sell, delta_size)

    logger.info("calculated orders grid:")
    for order in orders_sell + orders_buy:
        logger.info("  %4s %.2f @ %.4f" % (
            order.get('side'), order.get('size'), order.get('price')))

    calc_orders = orders_sell + orders_buy
    sourse_open_orders = client.get_open_orders()

    open_orders = [{'size': order.get('size'),
                    'price': order.get('price'),
                    'side': order.get('side')} for order in client.get_open_orders()]

    to_create = [{'size': order.get('size'),
                   'price': order.get('price'),
                   'side': order.get('side')} for order in calc_orders
                 if {'size': order.get('size'),
                     'price': order.get('price'),
                     'side': order.get('side')} not in open_orders]

    calc_orders = [{'size': order.get('size'),
                    'price': order.get('price'),
                    'side': order.get('side')} for order in calc_orders]
    to_cancel = [order.get('order_id') for order in sourse_open_orders
                 if {'size': order.get('size'),
                     'price': order.get('price'),
                     'side': order.get('side')} not in calc_orders]

    if len(to_cancel) > 0:
        logger.info("Canceling %d orders:" % (len(to_cancel)))
        for order in to_cancel:
            logger.info(f"  {order}")
            client.cancel_order(order)

    if len(to_create) > 0:
        logger.info("Creating %d orders:" % (len(to_create)))
        for order in to_create:
            responce = client.create_order(order)
            logger.info("  %4s %.2f @ %.4f" % (
                responce.get('side'), responce.get('size'), responce.get('price')))

    logger.info('====================')
    time.sleep(loop_interval)