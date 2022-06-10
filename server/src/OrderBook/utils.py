from enum import Enum
import bisect


# Enum for order types
class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"


# Enum for order sides
class OrderSides(Enum):
    BUY = "BUY"
    SELL = "SELL"


# Util class that wraps a list, with the following properties:
# - New elements are inserted at the "correct" index
#     This implies the list is always sorted, in ASC order
# - There are no duplicate elements
class SortedSet():
    def __init__(self):
        self.vals = []
        self.val_set = set()

    def insert(self, val):
        if val not in self.val_set:
            bisect.insort(self.vals, val)
            self.val_set.add(val)

    def remove(self, val):
        if val in self.val_set:
            self.vals.remove(val)
            self.val_set.remove(val)

    def __len__(self):
        return len(self.vals)

    def __getitem__(self, i):
        return self.vals[i]
