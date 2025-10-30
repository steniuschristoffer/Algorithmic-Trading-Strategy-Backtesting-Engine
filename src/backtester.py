# src/backtester.py

import queue
from.event import MarketEvent

class Backtester:
    """
    The main class to orchestrate the backtest.
    """
    def __init__(self, data_handler, strategy, portfolio, execution_handler):
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution_handler = execution_handler
        
        self.events = queue.Queue()
        self.signals = 0
        self.orders = 0
        self.fills = 0
        self.num_strats = 1

    def _run_backtest(self):
        """
        Executes the backtest.
        """
        print("Running Backtest...")
        while True:
            # Update the market data
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                break # Backtest is over

        print("Backtest Finished.")

    def _process_events(self):
        """
        The main event loop.
        """
        while True:
            try:
                event = self.events.get(False)
            except queue.Empty:
                break
            else:
                if event is not None:
                    if event.type == 'MARKET':
                        self.strategy.calculate_signals(event)
                        self.portfolio.update_timeindex(event)
                    elif event.type == 'SIGNAL':
                        self.signals += 1
                        self.portfolio.update_signal(event)
                    elif event.type == 'ORDER':
                        self.orders += 1
                        self.execution_handler.execute_order(event)
                    elif event.type == 'FILL':
                        self.fills += 1
                        self.portfolio.update_fill(event)