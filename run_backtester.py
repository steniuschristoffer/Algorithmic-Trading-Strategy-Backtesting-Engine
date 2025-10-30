# run_backtest.py

from src.backtester import Backtester
from src.portfolio import Portfolio
from src.data import YahooFinanceDataHandler
from src.strategy import MovingAverageCrossover
import queue

# Create placeholder objects for components we'll build in Epic 3
class PlaceholderExecutionHandler:
    def execute_order(self, event):
        print(f"EXECUTION: Pretending to execute order for {event.symbol}")

if __name__ == '__main__':
    # --- Configuration ---
    symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    initial_capital = 100000.0

    # The main event queue
    events_queue = queue.Queue()

    # --- Initialization ---
    # We now use our real DataHandler and Strategy
    data_handler = YahooFinanceDataHandler(events=None, symbol=symbol, start_date=start_date, end_date=end_date)
    strategy = MovingAverageCrossover(data_handler=data_handler, events=None, short_window=50, long_window=200)
    
    # The portfolio and execution handler are still simple for now
    portfolio = Portfolio(data_handler=data_handler, events=events_queue, initial_capital=initial_capital)
    execution_handler = PlaceholderExecutionHandler()

    # Initialize the backtester
    backtester = Backtester(
            data_handler=data_handler,
            strategy=strategy,
            portfolio=portfolio,
            execution_handler=execution_handler,
            events=events_queue
        )

    # Run the backtest
    backtester.simulate_trading()