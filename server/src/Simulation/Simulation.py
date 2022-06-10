from Simulation.OrderBook import Order, OrderBook
from Simulation.Trader import Trader
from Simulation.utils import OrderSides, OrderTypes
import random
import uuid

"""
Simulator for the stock market.
Accepts number of traders and their trade frequency.
Simulates a real world situation taken into account a companies sentiment and a trader's character.
"""
class Simulation():
    def __init__(self, stock_name="SIMPLE", ipo_price=100, num_traders=1000, freq=1):
        # Create an orderbook
        self.orderbook = OrderBook(stock_name, ipo_price)
        # Generate a random number of random traders
        self.traders = [self.get_random_trader() for _ in range(num_traders)]
        self.freq = freq
        self.sentiment = 0.5
    
    # Generate a trader with random market sensitivity
    def get_random_trader(self):
        return Trader(random.random())
    
    # Mimics a clock in a simulation, representing that some time has passed and traders have 
    # had a chance to submit their orders
    def next_tick(self, verbose=True):
        for trader in self.traders:
            # If the trader will trade then get their order and add it to the order_book
            if self.trader_will_trade(trader) and random.random() > 0.2:
                order = self.get_trader_order(trader)
                self.orderbook.add_order(order)
        if (verbose):
            print(f"Current price: {self.orderbook.curr_price}")

    # Determine whether the trader will trade based on the trader's sensitivity to the market and their caffeine level 
    def trader_will_trade(self, trader):
        caffeine_level = random.randint(1, 2)
        chicken_finger = trader.sensitivity * random.random() * caffeine_level
        return chicken_finger > 1

    # A series of calculations to determine what order the trader will send
    def get_trader_order(self, trader):
        buy = True
        # Chances a trader will follow the general market trend
        # I.e Buy is everyone else is buying vice versa
        follow_market = random.random() > 0.1
        buy_sentiment = self.sentiment > (0.5 + random.uniform(-0.02, 0.02))

        # If trader wants to follow the market trend and the general buy sentiment is bad
        # then the trader won't buy.
        # If the trader doesn't want to follow the market trend and the general buy sentiment is good
        # then the trader also won't place a buy order.
        if follow_market != buy_sentiment:
            buy = False

        # Chances of a trader changing their mind
        change_of_mind = random.random() > 0.9
        # If the trader changed their, then whether or not they will buy will be the opposite
        buy = not buy if change_of_mind else buy
        side = OrderSides.BUY if buy else OrderSides.SELL

        # If market is mild, sensitivity doesn't matter as much
        volatility = abs(self.sentiment - 0.5) + random.uniform(0.05, 0.1)
        scaler = trader.sensitivity * volatility * random.random()
        # A formula for the quantity of stocks a trader purchases
        quantity = 100 * scaler * random.uniform(0.4, 0.6)

        # We want more limit orders than market orders because we want to mimic the real world
        # Also want to avoid market orders clogging up
        if random.random() > 0.1:
            curr_price = self.orderbook.curr_price
            # Dela value to allow buy/selll prices to vary within reason
            delta = curr_price * volatility * 0.01
            # Multiplier that will be applied later on if the trader makes a bad decision
            delta_multiplier = 1 if buy else -1
            price = curr_price
            # Chances a trader will make a bad decision, if they do, apply the dela_multiplier
            bad_decision = random.random() < 0.1
            if bad_decision:
                delta_multiplier *= -1

            price += delta * delta_multiplier

            # Return the Order that the trader will place
            return Order(uuid.uuid4(), OrderTypes.LIMIT, side, quantity, price)
        else:
            return Order(uuid.uuid4(), OrderTypes.MARKET, side, quantity)
    
    def set_sentiment(self, new_sentiment):
        self.sentiment = new_sentiment
