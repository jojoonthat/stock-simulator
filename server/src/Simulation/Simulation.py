from Simulation.OrderBook import Order, OrderBook
from Simulation.Trader import Trader
from Simulation.utils import OrderSides, OrderTypes
import random
import uuid


class Simulation():
    def __init__(self, stock_name="SIMPLE", ipo_price=100, num_traders=1000, freq=1):
        self.orderbook = OrderBook(stock_name, ipo_price)
        self.traders = [self.get_random_trader() for _ in range(num_traders)]
        self.freq = freq
        self.sentiment = 0.5
    
    def get_random_trader(self):
        return Trader(random.random())
    
    def next_tick(self, verbose=True):
        for trader in self.traders:
            if self.trader_will_trade(trader) and random.random() > 0.2:
                order = self.get_trader_order(trader)
                self.orderbook.add_order(order)
        if (verbose):
            print(f"Current price: {self.orderbook.curr_price}")

    def trader_will_trade(self, trader):
        caffeine_level = random.randint(1, 2)
        chicken_finger = trader.sensitivity * random.random() * caffeine_level
        return chicken_finger > 1

    def get_trader_order(self, trader):
        buy = True

        follow_market = random.random() > 0.1
        buy_sentiment = self.sentiment > (0.5 + random.uniform(-0.02, 0.02))

        if follow_market != buy_sentiment:
            buy = False

        change_of_mind = random.random() > 0.9
        buy = not buy if change_of_mind else buy
        side = OrderSides.BUY if buy else OrderSides.SELL

        # If market is mild, sensitivity doesn't matter as much
        volatility = abs(self.sentiment - 0.5) + random.uniform(0.05, 0.1)
        scaler = trader.sensitivity * volatility * random.random()

        quantity = 100 * scaler * random.uniform(0.4, 0.6)

        if random.random() > 0.1:
            curr_price = self.orderbook.curr_price
            delta = curr_price * volatility * 0.01
            delta_multiplier = 1 if buy else -1
            price = curr_price
            
            bad_decision = random.random() < 0.1
            if bad_decision:
                delta_multiplier *= -1

            price += delta * delta_multiplier

            return Order(uuid.uuid4(), OrderTypes.LIMIT, side, quantity, price)
        else:
            return Order(uuid.uuid4(), OrderTypes.MARKET, side, quantity)
    
    def set_sentiment(self, new_sentiment):
        self.sentiment = new_sentiment
