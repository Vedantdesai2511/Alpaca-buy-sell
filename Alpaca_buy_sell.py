import alpaca_trade_api as tradeapi
import config


class AlpacaBuySell:

    def __init__(self, symbol=None, qty=10, order_type='market', time_in_force='gtc'):
        self.base_url = config.BASE_URL
        self.api_key_id = 'PKFK5ZG1GL1U1Y66UHU1'  # put your api key of the account you want to trade on
        self.api_secret = 'lG1oalOi1nEUFkTQNtU3QRkBm1bnDvABlRYhYZnm'  # put your secret key of the account you want
        # to trade on
        self.symbol = symbol  # Ticker symbol of the stock
        self.qty = qty  # number of shares
        self.order_type = order_type  # Order type
        self.time_in_force = time_in_force  # Time in force

    def api_call(self):  # This function uses api call to get to the endpoint from which user can buy/sell stocks
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        return api

    def naked_buy_order(self):  # Place a naked buy order
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # lace a naked buy order i.e. place a market buy order without any limit or stop sell order
        naked_buy_order = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='simple',
        )

        return naked_buy_order

    def buy(self, limit, stop):  # Place market buy order with limit and stop (OCO) orders
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        #  place market order along with take profit and stop limit order
        api_buy = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='bracket',
            take_profit=dict(limit_price=limit),
            stop_loss=dict(stop_price=stop)
        )

        return api_buy

    def buy_and_stop_order(self, stop):  # Place buy with stop loss order
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market order along with take profit and stop limit order
        api_buy = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='oto',
            stop_loss=dict(stop_price=stop)
        )

        return api_buy

    def stop_limit_buy_order(self, limit_price, stop_price):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market order along with take profit and stop limit order
        api_buy = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='oto',
            stop_loss=dict(stop_price=stop_price, limit_price=limit_price)
        )

    def stop_limit_sell_order(self, limit, stop):  # place market sell order take profit and stop limit order
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market sell order take profit and stop limit order

        api_stop_limit_sell = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='limit',
            time_in_force=self.time_in_force,
            order_class='oco',
            take_profit=dict(limit_price=limit),
            stop_loss=dict(stop_price=stop)
        )

        return api_stop_limit_sell

    def stop_limit_buy_order_without_making_a_market_buy(self, limit, stop):  # Place stop and limit (OCO) orders
        # without placing a buy order for this to work one must have a open naked buy order
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        api_buy = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type='limit',
            time_in_force=self.time_in_force,
            order_class='oco',
            take_profit=dict(limit_price=limit),
            stop_loss=dict(stop_price=stop)
        )

    def market_sell(self):  # Redundant function due to some dependancy I did not remove it but you can use short
        # sell instead of this function
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market order along with take profit and stop limit order
        api_sell = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='market',
            time_in_force=self.time_in_force,
            # limit_price = limit
        )

        return api_sell

    def short_sell(self):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market order along with take profit and stop limit order
        api_sell = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='market',
            time_in_force=self.time_in_force,
            # limit_price = limit
        )

        return api_sell

    def limit_sell(self, limit):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )
        # place market order along with take profit and stop limit order
        api_sell = api.submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='limit',
            time_in_force=self.time_in_force,
            limit_price=limit
        )

        return api_sell

    def current_positions(self):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        positions = api.list_positions()

        for idx, p in enumerate(positions):
            if positions[idx].symbol != self.symbol:
                return False
            else:
                return True

    def liqidate_positions(self):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        orders = api.list_orders(status='open')
        positions = api.list_positions()

        if orders or positions:
            if positions:
                print(positions)

            if orders:
                print("Canceling open orders:")
                print([o.id for o in orders])
                result = [api.cancel_order(o.id) for o in orders]
                print(result)

            closed = []
            for p in positions:
                side = 'sell'
                if int(p.qty) < 0:
                    p.qty = abs(int(p.qty))
                    side = 'buy'
                closed.append(
                    api.submit_order(p.symbol, qty=p.qty, side=side, type="market", time_in_force="day")
                )

            if closed:
                print("Submitted Orders", closed)

            for o in closed:
                status = api.get_order(o.id)
                if status.status == 'rejected':
                    print("ORDER FAILED: Your Order was Rejected!!!")

    def liqidate_position_of_a_stock(self):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        pos = api.list_positions()
        # print(pos[0].symbol)
        for idx, p in enumerate(pos):
            if pos[idx].symbol == self.symbol:
                print("Element Exists")
                print(pos[idx].symbol)
                print(pos[idx].side)
                print(pos[idx].qty)
                if pos[idx].side == "long":
                    print("I am here")
                    AlpacaBuySell(pos[idx].symbol, qty=pos[idx].qty).market_sell()

    def cancel_orders_and_liquidate_the_given_stock(self):
        api = tradeapi.REST(
            base_url=self.base_url,
            key_id=self.api_key_id,
            secret_key=self.api_secret
        )

        order_list_for_the_give_stock = list()

        list_orders_ = api.list_orders()
        for i in list_orders_:
            if i.symbol == self.symbol:
                order_list_for_the_give_stock.append(i.id)
                # print(i.id[-1])

        print(order_list_for_the_give_stock)
        api.cancel_order(order_list_for_the_give_stock[-1])
        # AlpacaBuySell(self.symbol).liqidate_position_of_a_stock()

        pos = api.list_positions()
        for idx, p in enumerate(pos):
            if pos[idx].symbol == self.symbol:
                print("Element Exists")
                print(pos[idx].symbol)
                print(pos[idx].side)
                # print(pos[idx].qty)
                if pos[idx].side == "long":
                    print("I am here")
                    AlpacaBuySell(pos[idx].symbol, qty=self.qty).market_sell()


# Below are the testing codes for diffrent scenarios

# api = AlpacaBuySell().api_call()
# list_orders = api.list_orders()
# print(list_orders)
# AlpacaBuySell("ZM").cancel_orders_and_liquidate_the_given_stock()
# print(list_orders[1].id[-1])
# api = tradeapi.REST(
#     base_url=config.Liquidate_all_the_positions_url,
#     key_id=config.API_KEY,
#     secret_key=config.SECRET_KEY
# )

# import requests

# HEADERS = {
#     'APCA-API-KEY-ID': 'PKFK5ZG1GL1U1Y66UHU1',
#     'APCA-API-SECRET-KEY': 'lG1oalOi1nEUFkTQNtU3QRkBm1bnDvABlRYhYZnm'
# }

# day_bars_url = '{}/day?symbols=&limit=5'.format(config.Liquidate_all_the_positions_url)

# r = requests.delete(config.Liquidate_all_the_positions_url, headers=HEADERS)

# limit = 140.0
# limit = str(limit)
# stop = 200.0
# stop = str(stop)
# AlpacaBuySell("ROKU").stop_limit_buy_order_without_making_a_market_buy(limit, stop)
# # AlpacaBuySell('OSTK', qty=100).naked_buy_order()
# # AlpacaBuySell('OSTK', qty=100).stop_limit_sell_order(limit, stop)
# # AlpacaBuySell("ROKU").short_sell()
# AlpacaBuySell("FB", qty=1).stop_limit_buy_order_without_making_a_market_buy(limit=limit, stop=stop)

###########################################################################################

# import time
# #
# #
# api = AlpacaBuySell().api_call()
# list_orders = api.list_orders()
# for idx, i in enumerate(list_orders):
#     # print(i)
#     if i.symbol == "OSTK":
#         print(i.id)
#         api.cancel_order(i.id)
#         AlpacaBuySell("OSTK").liqidate_position_of_a_stock()
# print(list_orders[1].symbol)
# print(list_orders[1]['symbol'])
# AlpacaBuySell("SRNE").liqidate_position_of_a_stock()
# api.cancel_order('a65dfcd8-7419-4ff3-a433-7bc178b42dcc')
# a = AlpacaBuySell("ROKU").short_sell()
# print(a)
# time.sleep(1)
# MAke a thread which just keeps on tracking the trailing stop loss #

# x = 123.0
# x = str(x)
# a = AlpacaBuySell("ROKU").stop_limit_sell_order(limit='129.0', stop=x)
# print(a.id)
# print(a)
# time.sleep(5)
# api.cancel_order(order_id=str(a.id))
# time.sleep(5)
# x = 124.0
# x = str(x)
# a = AlpacaBuySell("ROKU").stop_limit_sell_order(limit='129.0', stop=x)
# print(a.id)
# # a = AlpacaBuySell("ROKU").buy_and_stop_order(127.0)
# time.sleep(0.2)


###########################################################################################

# C:\Users\vedan\AppData\Local\Programs\Python\Python38-32\python.exe C:/Users/vedan/PycharmProjects/up_down_fib_code/Alpaca_buy_sell.py
# Order({   'asset_class': 'us_equity',
#     'asset_id': 'c527d9ac-b902-4dca-89c1-b6735e7460de',
#     'canceled_at': None,
#     'client_order_id': '720e22b1-ee67-4c52-842a-e51030c412ef',
#     'created_at': '2020-07-02T13:57:07.419954Z',
#     'expired_at': None,
#     'extended_hours': False,
#     'failed_at': None,
#     'filled_at': None,
#     'filled_avg_price': None,
#     'filled_qty': '0',
#     'id': '7d82b36c-1162-4fba-9a48-d7fa9ee891f2',
#     'legs': [   {   'asset_class': 'us_equity',
#                     'asset_id': 'c527d9ac-b902-4dca-89c1-b6735e7460de',
#                     'canceled_at': None,
#                     'client_order_id': 'cb4b3225-3c4b-4513-8ee7-c55251556810',
#                     'created_at': '2020-07-02T13:57:07.419954Z',
#                     'expired_at': None,
#                     'extended_hours': False,
#                     'failed_at': None,
#                     'filled_at': None,
#                     'filled_avg_price': None,
#                     'filled_qty': '0',
#                     'id': '758ac258-f655-44f9-bb23-e49bdc737a2d',
#                     'legs': None,
#                     'limit_price': None,
#                     'order_class': 'oco',
#                     'order_type': 'stop',
#                     'qty': '100',
#                     'replaced_at': None,
#                     'replaced_by': None,
#                     'replaces': None,
#                     'side': 'sell',
#                     'status': 'held',
#                     'stop_price': '126',
#                     'submitted_at': '2020-07-02T13:57:07.409383Z',
#                     'symbol': 'ROKU',
#                     'time_in_force': 'gtc',
#                     'type': 'stop',
#                     'updated_at': '2020-07-02T13:57:07.419954Z'}],
#     'limit_price': '129',
#     'order_class': 'oco',
#     'order_type': 'limit',
#     'qty': '100',
#     'replaced_at': None,
#     'replaced_by': None,
#     'replaces': None,
#     'side': 'sell',
#     'status': 'accepted',
#     'stop_price': None,
#     'submitted_at': '2020-07-02T13:57:07.409383Z',
#     'symbol': 'ROKU',
#     'time_in_force': 'gtc',
#     'type': 'limit',
#     'updated_at': '2020-07-02T13:57:07.447987Z'})
