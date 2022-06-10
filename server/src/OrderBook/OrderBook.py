from collections import defaultdict
from utils import OrderType, OrderSides, SortedSet


"""
Order to be added into an OrderBook instance for matching.
"""
class Order:
    def __init__(self, order_id, order_type, side, quantity, price=None):
        self.id = order_id
        
        # Market / Limit
        self.type = order_type

        # Buy / Sell
        self.side = side

        self.orig_quantity = quantity
        self.quantity = quantity

        if order_type == OrderType.LIMIT:
            self.price = price
        else:
            # +inf / -inf if market order is buy / sell
            price = "inf" if side == OrderSides.BUY else "-inf"
            self.price = float(price)


"""
OrderBook for a stock.
Accepts both market and limit orders.
Performs stock-matching based on FIFO price-time algo.
I.e. Orders take priority in the order of price and time.
"""
class OrderBook:
    def __init__(self, name, ipo_price):
        self.name = name
        self.curr_price = ipo_price

        # Map price to dict, which itself maps order id to order
        self.buys = defaultdict(dict)
        self.sorted_buy_prices = SortedSet()
        self.sells = defaultdict(dict)
        self.sorted_sell_prices = SortedSet()

        # Dict to keep track of active orders to make removing them easier
        self.live_order_ids = {}

    @property
    def best_buy(self):
        # Highest buy price
        no_buys = len(self.buys) == 0
        return float("-inf") if no_buys else self.sorted_buy_prices[-1]

    @property
    def best_sell(self):
        # Lowest sell price
        no_sells = len(self.sells) == 0
        return float("inf") if no_sells else self.sorted_sell_prices[0]

    # Add order to book
    def add_order(self, order: Order):
        # Add order to keep track
        self.live_order_ids[order.id] = [order.price, order.side]

        # Limit order
        if order.type == OrderType.LIMIT:
            if order.side == OrderSides.BUY:
                # Only initiate matching when there is a equal or lower sell order
                if order.price >= self.best_sell:
                    self.execute_match(order)
                # If part or all of order is unfulfilled
                if order.quantity > 0:
                    # Store remaining order and add price to sorted price list
                    self.buys[order.price][order.id] = order
                    self.sorted_buy_prices.insert(order.price)
            else:
                # Limit sell
                # Only initiate matching when there is a equal or higher buy order
                if order.price <= self.best_buy:
                    self.execute_match(order)
                # If part of all of order is unfulfilled
                if order.quantity > 0:
                    # Store remaining order and add price to sorted price list
                    self.sells[order.price][order.id] = order
                    self.sorted_sell_prices.insert(order.price)
            return

        # Market Order
        if order.type == OrderType.MARKET:
            # Match right away
            self.execute_match(order)
            if order.quantity > 0:
                # Order partially / fully unfulfilled
                # Store remaining order and add price to sorted price list
                if order.side == OrderSides.BUY:
                    self.buys[order.price][order.id] = order
                    self.sorted_buy_prices.insert(order.price)
                else:
                    # Market sell
                    self.sells[order.price][order.id] = order
                    self.sorted_sell_prices.insert(order.price)

    # Remove active order given order id
    def remove_order(self, order_id):
        price, side = self.live_order_ids[order_id]
        # Determine whether the remove_id order is in self.buys or self.sells
        orders = self.buys if side == OrderSides.BUY else self.sells
        prices = self.sorted_buy_prices if side == OrderSides.BUY else self.sorted_sell_prices

        self.live_order_ids.pop(order_id)
        prices.remove(price)
        orders[price].pop(order_id)

        # There could be 0 order at this price. Delete price key if this is the case.
        if len(orders[price]) == 0:
            orders.pop(price)

    # Check if two order prices can be matched
    def is_match(self, side, order_price, target_price):
        if side == OrderSides.BUY:
            return order_price >= target_price
        else:
            # Sell order
            return order_price <= target_price

    # Match current order book, if possible
    def execute_match(self, order):
        orders = self.buys if order.side == OrderSides.SELL else self.sells
        prices, prices_iters = None, None
        if order.side == OrderSides.BUY:
            # Buy order. We'll iterate sell prices in ASC order for matching
            prices = self.sorted_sell_prices
            prices_iters = prices.vals
        else:
            # Sell order. We'll iterate buy prices in DESC order for matching
            prices = self.sorted_buy_prices
            prices_iters = reversed(prices.vals)

        for price in prices_iters:
            unfulfilled = order.quantity > 0
            match = self.is_match(order.side, order.price, price)

            # Continue iff there is still quantity to fulfill, and the order price and target price match
            if not (unfulfilled and match):
                break

            # Avoid python re-eval dict keys during iteration by casting to list
            resting_order_ids = list(orders[price].keys())    
            for resting_order_id in resting_order_ids:
                # If order is fulfilled, bail
                if order.quantity == 0:
                    break

                # A resting order is an order at current price in the order book,
                # that can be matched to the current order
                resting_order = orders[price][resting_order_id]

                # Two orders can be matched. Adjust unfulfilled quantity accordingly
                size = min(order.quantity, resting_order.quantity)
                order.quantity -= size
                resting_order.quantity -= size

                # The resting order may be fulfilled. Remove if so
                if resting_order.quantity == 0:
                    orders[price].pop(resting_order_id)
                
                # If we didn't just match two market orders, update current price
                if not(order.type == OrderType.MARKET and resting_order.type == OrderType.MARKET):
                    self.curr_price = price
            
            # Remove price key if there are no more orders at that price
            if len(orders[price]) == 0:
                orders.pop(price)
                prices.remove(price)
