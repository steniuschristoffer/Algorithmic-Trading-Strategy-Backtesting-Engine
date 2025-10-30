# src/event.py

class Event:
    """
    Base class for all event types.
    """
    pass

class MarketEvent(Event):
    """
    Handles the event of receiving new market data for a bar.
    """
    def __init__(self):
        self.type = 'MARKET'

class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """
    def __init__(self, symbol, datetime, signal_type):
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type  # 'LONG', 'SHORT', 'EXIT'

class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol, a type (market or limit), quantity and direction.
    """
    def __init__(self, symbol, order_type, quantity, direction):
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type  # 'MKT' or 'LMT'
        self.quantity = quantity
        self.direction = direction  # 'BUY' or 'SELL'

class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage.
    Stores the quantity of an instrument actually filled and at what price.
    In addition, it stores the commission of the trade from the brokerage.
    """
    def __init__(self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=0.0):
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission