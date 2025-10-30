# src/backtester.py

import queue
from.event import MarketEvent

class Backtester:
    """
    The main class to orchestrate the backtest.
    """
    def __init__(self, data_handler, strategy, portfolio, execution_handler, events):
        self.data_handler = data_handler
        self.strategy = strategy
        self.portfolio = portfolio
        self.execution_handler = execution_handler
        self.events = events # Use the passed-in events queue
        
        
        # Pass the event queue to the components that need it
        self.data_handler.events = self.events
        self.strategy.events = self.events

    def run_backtest(self):
        """
        Executes the backtest.
        """
        print("Running Backtest...")
        
        # Main event loop
        while True:
            # 1. Get new market data
            if self.data_handler.continue_backtest:
                self.data_handler.update_bars()
            else:
                print("Backtest over")
                break # Backtest is over

            # 2. Process all events in the queue
            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            # Market events trigger the strategy to calculate signals
                            self.strategy.calculate_signals(event)
                            # And the portfolio to update its value
                            self.portfolio.update_timeindex(event)
                        elif event.type == 'SIGNAL':
                            # Signal events are handled by the portfolio
                            self.portfolio.update_signal(event)
                        elif event.type == 'ORDER':
                            # Order events are handled by the execution handler
                            self.execution_handler.execute_order(event)
                        elif event.type == 'FILL':
                            # Fill events are handled by the portfolio
                            self.portfolio.update_fill(event)
        
        print("Backtest Finished.")

    def simulate_trading(self):
        """
        A simpler alias for run_backtest for clarity.
        """
        self.run_backtest()