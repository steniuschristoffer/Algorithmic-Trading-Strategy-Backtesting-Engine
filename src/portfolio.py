# src/portfolio.py

import pandas as pd

class Portfolio:
    """
    Manages the portfolio's state, including cash, holdings, and total value.
    """
    def __init__(self, initial_capital=100000.0):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.holdings = {}  # Dictionary to store current holdings (ticker: quantity)
        self.positions = pd.DataFrame() # To store historical positions and values

    def update_timeindex(self, event):
        """
        Updates the portfolio value based on the latest market data.
        This would be called on each MarketEvent.
        """
        # In a real scenario, this method would update the market value
        # of all current holdings. For now, it's a placeholder.
        print(f"Portfolio is being updated at a new timeindex...")
        pass

    def update_fill(self, event):
        """
        Updates the portfolio's holdings and cash based on a FillEvent.
        """
        # This is where we would adjust cash and holdings after a trade.
        # We will implement this in a later story.
        print(f"Portfolio is updating based on a fill event...")
        pass