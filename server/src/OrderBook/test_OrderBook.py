from utils import OrderType, OrderSides
from OrderBook import OrderBook, Order


# test if precendence of orders being fulfilled is correct
def test_curr_price_limit_orders():
    order = Order(0, OrderType.LIMIT, OrderSides.SELL, 20, 30)
    order1 = Order(1, OrderType.LIMIT, OrderSides.SELL, 10, 40)
    order2 = Order(2, OrderType.LIMIT, OrderSides.BUY, 20, 20)
    order3 = Order(3, OrderType.LIMIT, OrderSides.BUY, 20, 50)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)
    order_book.add_order(order2)
    order_book.add_order(order3)

    assert(order_book.curr_price == 30)

# test if curr_price is correct and limit + market matching behaviour is correct
def test_curr_price_market_orders():
    order = Order(0, OrderType.LIMIT, OrderSides.SELL, 20, 60)
    order1 = Order(1, OrderType.MARKET, OrderSides.BUY, 20)
    order2 = Order(2, OrderType.MARKET, OrderSides.BUY, 30)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)
    order_book.add_order(order2)

    assert(order_book.curr_price == 60)

# test if curr_price is correct and limit + limit matching behaviour is correct
def test_curr_price_all_orders():
    order = Order(0, OrderType.LIMIT, OrderSides.SELL, 20, 70)
    order1 = Order(1, OrderType.LIMIT, OrderSides.BUY, 20, 50)
    order2 = Order(2, OrderType.MARKET, OrderSides.BUY, 20)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)
    order_book.add_order(order2)

    assert(order_book.curr_price == 70)

# test if market order is considered best_sell over limit order
def test_order_book_best_sell():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order1 = Order(1, OrderType.LIMIT, OrderSides.SELL, 50, 30)
    order2 = Order(2, OrderType.MARKET, OrderSides.SELL, 20)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)
    order_book.add_order(order2)

    assert(order_book.best_sell == float("-inf"))

# test if market order gets fulfilled first
def test_order_book_best_buy():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order1 = Order(1, OrderType.LIMIT, OrderSides.SELL, 50, 30)
    order2 = Order(2, OrderType.LIMIT, OrderSides.BUY, 20, 10)
    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)
    order_book.add_order(order2)

    assert(order_book.best_buy == 10)

# test if order_book.buys properly stores buy entries and if the match is unsuccessful as expected
def test_order_book_buy_list():
    order = Order(0, OrderType.LIMIT, OrderSides.SELL, 20, 40)
    order1 = Order(1, OrderType.LIMIT, OrderSides.BUY, 20, 30)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)

    assert(bool(order_book.buys) == True)

# test if order_book.sells properly stores sell entries and if the match is unsuccessful as expected
def test_order_book_sell_list():
    order = Order(0, OrderType.LIMIT, OrderSides.SELL, 20, 40)
    order1 = Order(1, OrderType.LIMIT, OrderSides.BUY, 20, 30)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)

    assert(bool(order_book.sells) == True)

# test if order_book.buys properly stores buy entries
def test_one_market_order():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order_book = OrderBook("U", 100)
    order_book.add_order(order)

    assert(bool(order_book.buys) == True)

# test edge case where there are only market orders, curr_price should remain the same
def test_market_buy_sell_match_price():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order1 = Order(1, OrderType.MARKET, OrderSides.SELL, 20)

    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)

    assert(order_book.curr_price == 100)

# test edge case where there are only market orders
def test_market_buy_sell_match():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order1 = Order(1, OrderType.MARKET, OrderSides.SELL, 20)
    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.add_order(order1)

    assert(bool(order_book.buys) == False)

# test remove_order function
def test_remove_order():
    order = Order(0, OrderType.MARKET, OrderSides.BUY, 20)
    order_book = OrderBook("U", 100)
    order_book.add_order(order)
    order_book.remove_order(0)

    assert(bool(order_book.buys) == False)
