# src/strategy.py

from abc import ABC, abstractmethod
import pandas as pd

from.event import SignalEvent

class Strategy(ABC):
    """
    Abstract base class for trading strategies.
    """
    def __init__(self, data_handler, events):
        self.data_handler = data_handler
        self.events = events
        self.bought = self._calculate_initial_bought()

    @abstractmethod
    def calculate_signals(self, event):
        """Provides the mechanisms to calculate the list of signals."""
        raise NotImplementedError("Should implement calculate_signals()")

    def _calculate_initial_bought(self):
        """Adds keys to the bought dictionary for all symbols and sets them to 'OUT'."""
        bought = {}
        # For now, we assume a single symbol from the data_handler
        bought[self.data_handler.symbol] = 'OUT'
        return bought

class MovingAverageCrossover(Strategy):
    """
    A simple moving average crossover strategy.
    """
    def __init__(self, data_handler, events, short_window=50, long_window=200):
        super().__init__(data_handler, events)
        self.short_window = short_window
        self.long_window = long_window

    def calculate_signals(self, event):
        """
        Generates a buy signal if the short moving average crosses above the long,
        and a sell signal if it crosses below.
        """
        if event.type == 'MARKET':
            symbol = self.data_handler.symbol
            bars = self.data_handler.get_latest_bars(symbol, N=self.long_window)

            if len(bars) >= self.long_window:
                short_sma = bars['Close'].tail(self.short_window).mean()
                long_sma = bars['Close'].mean()

                # Trading logic
                if short_sma[symbol] > long_sma[symbol] and self.bought[symbol] == 'OUT':
                    print(f"BUY SIGNAL: {bars.index[-1]}")
                    signal = SignalEvent(symbol, bars.index[-1], 'LONG')
                    self.events.put(signal)
                    self.bought[symbol] = 'LONG'
                elif short_sma[symbol] < long_sma[symbol] and self.bought[symbol] == 'LONG':
                    print(f"SELL SIGNAL: {bars.index[-1]}")
                    signal = SignalEvent(symbol, bars.index[-1], 'EXIT')
                    self.events.put(signal)
                    self.bought[symbol] = 'OUT'