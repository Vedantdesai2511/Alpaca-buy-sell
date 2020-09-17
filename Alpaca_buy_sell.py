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

    def naked_buy_order(self):
        """
        place a naked buy order i.e. place a market buy order without any limit or stop sell order
        """
        naked_buy_order = AlpacaBuySell(self.symbol).api_call().submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='simple',
        )

        return naked_buy_order

    def buy(self, limit, stop):
        """
        Place market buy order with limit and stop (OCO) orders
        i.e. place market order along with take profit and stop limit order
        """
        api_buy = AlpacaBuySell(self.symbol).api_call().submit_order(
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

    def buy_and_stop_order(self, stop):
        """
        Place buy with stop loss order
        """
        api_buy = AlpacaBuySell(self.symbol).api_call().submit_order(
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
        """
        place market buy order along with take profit and stop limit order
        """
        api_buy = AlpacaBuySell(self.symbol).api_call().submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='buy',
            type=self.order_type,
            time_in_force=self.time_in_force,
            order_class='oto',
            stop_loss=dict(stop_price=stop_price, limit_price=limit_price)
        )

        return api_buy

    def stop_limit_sell_order(self, limit, stop):
        """
        place market sell order take profit and stop limit order
        """
        api_stop_limit_sell = AlpacaBuySell(self.symbol).api_call().submit_order(
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

    def stop_limit_buy_order_without_making_a_market_buy(self, limit, stop):
        """
        Place stop and limit (OCO) orders
        without placing a buy order for this to work one must have a open naked buy order
        """
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

        return api_buy

    def market_sell(self):
        """
        Place market sell order - to close out the long position in particular stock
        """
        api_sell = AlpacaBuySell(self.symbol).api_call().submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='market',
            time_in_force=self.time_in_force,
        )

        return api_sell

    def short_sell(self):
        """
        Place short sell order on the given stock
        Caution: If the broken does not allow shorting on the given stock you will not be able to short that stock.
        """
        api_sell = AlpacaBuySell(self.symbol).api_call().submit_order(
            symbol=self.symbol,
            qty=self.qty,
            side='sell',
            type='market',
            time_in_force=self.time_in_force,
        )

        return api_sell

    def limit_sell(self, limit):
        """
        place market order along with take profit and stop limit order
        """
        api_sell = AlpacaBuySell(self.symbol).api_call().submit_order(
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
        """
            This function liquidates all the naked orders present in the current account (portfolio)
        """

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
        """
            This function liquidates the naked position of the specified stock
        """

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
        """
            This function liquidates EVERYTHING (i.e. ALL the orders) all the naked orders and all the oco orders too.
        """
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
                    # print("I am here")
                    AlpacaBuySell(pos[idx].symbol, qty=self.qty).market_sell()
                elif pos[idx].side == "short":
                    AlpacaBuySell(pos[idx].symbol, qty=self.qty).naked_buy_order()


