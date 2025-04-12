# engine/data.py
import pandas as pd
import numpy as np
import yfinance as yf

def fetch_real_data(tickers, start_date="2021-05-12", end_date="2022-05-12"):
    """
    Fetch historical adjusted close prices from Yahoo Finance.
    
    Parameters:
    - tickers: list of str, stock tickers (e.g., ['ADRO.JK', 'ASII.JK']).
    - start_date: str, start date in YYYY-MM-DD format.
    - end_date: str, end date in YYYY-MM-DD format.
    
    Returns:
    - pandas DataFrame with dates as index and tickers as columns.
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Close']
        # return data.dropna()
        return data
    except Exception as e:
        raise ValueError(f"Failed to fetch data: {e}")

def compute_returns(prices):
    """
    Compute daily percentage returns from price data.
    
    Parameters:
    - prices: pandas DataFrame with dates as index and tickers as columns.
    
    Returns:
    - pandas DataFrame of daily returns.
    """
    returns = prices.pct_change().dropna()
    return returns

# def generate_synthetic_data(tickers, start_date="2021-05-12", end_date="2022-05-12", base_price=100, volatility=0.01):
#     """
#     Generate synthetic price data for testing.
    
#     Parameters:
#     - tickers: list of str, stock tickers.
#     - start_date: str, start date.
#     - end_date: str, end date.
#     - base_price: float, starting price for all stocks.
#     - volatility: float, standard deviation of daily returns.
    
#     Returns:
#     - pandas DataFrame with dates as index and tickers as columns.
#     """
#     dates = pd.date_range(start=start_date, end=end_date, freq="B")
#     prices = pd.DataFrame(
#         np.random.randn(len(dates), len(tickers)) * volatility + base_price,
#         index=dates,
#         columns=tickers
#     ).cumsum()
#     return prices