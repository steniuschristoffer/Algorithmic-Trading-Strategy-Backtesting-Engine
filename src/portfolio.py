# src/portfolio.py

import pandas as pd
from.event import OrderEvent

class Portfolio:
    """
    Manages the portfolio's state, including cash, holdings, and total value.
    """
    def __init__(self, data_handler, events, initial_capital=100000.0):
        self.data_handler = data_handler
        self.events = events
        self.initial_capital = initial_capital
        self.cash = initial_capital
        
        # Holds the current quantity of a symbol
        if isinstance(self.data_handler.symbol, str):
            # If it is, put that single string into a new list
            symbols_list = [self.data_handler.symbol]
        else:
            # Otherwise, assume it's already a list (like ['AAPL', 'GOOG'])
            symbols_list = self.data_handler.symbol
            
        self.current_holdings = {symbol: 0 for symbol in symbols_list}
        print(self.current_holdings)

    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders.
        """
        if event.type == 'SIGNAL':
            order_event = self._generate_order(event)
            if order_event:
                self.events.put(order_event)

    def _generate_order(self, signal):
        """
        Generates an OrderEvent based on a SignalEvent.
        For now, uses a simple fixed quantity of 100 shares.
        """
        order = None
        symbol = signal.symbol
        direction = None
        
        # Simple logic: 100 shares for a LONG signal, sell all for an EXIT signal
        quantity = 100
        current_quantity = self.current_holdings[symbol]

        if signal.signal_type == 'LONG' and current_quantity == 0:
            direction = 'BUY'
            print(f"PORTFOLIO: Generating BUY order for {quantity} shares of {symbol}")
            order = OrderEvent(symbol, 'MKT', quantity, direction)
        
        elif signal.signal_type == 'EXIT' and current_quantity > 0:
            direction = 'SELL'
            quantity = current_quantity # Sell all shares we currently hold
            print(f"PORTFOLIO: Generating SELL order for {quantity} shares of {symbol}")
            order = OrderEvent(symbol, 'MKT', quantity, direction)
            
        return order

    def update_timeindex(self, event):
        """
        Updates the portfolio value based on the latest market data.
        This would be called on each MarketEvent.
        """
        # In a real scenario, this method would update the market value
        # of all current holdings. For now, it's a placeholder.
        pass

    def update_fill(self, event):
        """
        Updates the portfolio's holdings and cash based on a FillEvent.
        """
        # This is where we would adjust cash and holdings after a trade.
        # We will implement this in a later story.
        print(f"Portfolio is updating based on a fill event...")
        pass