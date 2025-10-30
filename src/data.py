# src/data.py

from abc import ABC, abstractmethod
import pandas as pd
import yfinance as yf

from.event import MarketEvent

class DataHandler(ABC):
    """
    Abstract base class for handling market data.
    """
    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """Returns the last N bars from the data feed."""
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self):
        """Pushes the latest bar to the event queue."""
        raise NotImplementedError("Should implement update_bars()")

class YahooFinanceDataHandler(DataHandler):
    """
    Handles data from Yahoo Finance.
    """
    def __init__(self, events, symbol, start_date, end_date):
        self.events = events
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = self._get_data()
        self.latest_symbol_data = None
        self.continue_backtest = True
        self._bar_iterator = self.data.iterrows()

    def _get_data(self):
        """Fetches and returns the historical data from Yahoo Finance."""
        try:
            data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
            return data.sort_index()
        except Exception as e:
            print(f"Could not download data for {self.symbol}: {e}")
            return pd.DataFrame()

    def get_latest_bars(self, symbol, N=1):
        """Returns the last N bars from the latest_symbol_data."""
        if symbol == self.symbol:
            try:
                return self.latest_symbol_data.tail(N)
            except AttributeError:
                # This can happen if latest_symbol_data is not yet a DataFrame
                return pd.DataFrame()
        return pd.DataFrame()

    def update_bars(self):
        """Pushes the next bar from the data feed into the event queue."""
        try:
            index, bar = next(self._bar_iterator)
            if self.latest_symbol_data is None:
                self.latest_symbol_data = pd.DataFrame([bar], index=[index])
            else:
                self.latest_symbol_data.loc[index] = bar
            
            # Create a MarketEvent and put it on the queue
            self.events.put(MarketEvent())
        except StopIteration:
            self.continue_backtest = False