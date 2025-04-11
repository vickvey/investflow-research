import os
import sys
import pandas as pd
import yfinance as yf

# Add the 'engine' folder to the sys.path to ensure that Python can find the module
sys.path.append(os.path.join(os.path.dirname(__file__), 'engine'))

# Now we can import the fetch_real_data function from data.py
from data import fetch_real_data  # Import the fetch_real_data function from your code

# Function to download stock data from Yahoo Finance and save it as a CSV
def download_data_to_csv(tickers, start_date="2021-05-12", end_date="2022-05-12", filename="stock_data.csv"):
    try:
        print("Downloading data from Yahoo Finance...")
        # Download data using yfinance
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']
        
        if data.empty:
            print("Error: No data returned for tickers. Check ticker symbols or date range.")
            return
        
        # Save the data to CSV
        data.to_csv(filename)
        print(f"Data successfully downloaded and saved to {filename}.")
    except Exception as e:
        print(f"Error downloading data: {e}")

# Function to load the CSV file and compare it with the fetched data
def compare_data(csv_filename, tickers, start_date="2021-05-12", end_date="2022-05-12"):
    print("\nStarting data comparison...")

    # Load the downloaded CSV file
    try:
        print(f"Loading CSV data from {csv_filename}...")
        csv_data = pd.read_csv(csv_filename, parse_dates=['Date'], index_col='Date')
        
        # Check if the tickers are in the columns of the CSV data
        missing_tickers = [ticker for ticker in tickers if ticker not in csv_data.columns]
        if missing_tickers:
            print(f"Warning: Missing tickers in CSV file: {missing_tickers}")
            return

    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
        return
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Fetch data using the original fetch_real_data function
    print("Fetching data using fetch_real_data function...")
    try:
        fetched_data = fetch_real_data(tickers, start_date, end_date)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # Ensure both dataframes have the same date range
    if not csv_data.index.equals(fetched_data.index):
        print("Date ranges do not match.")
        print(f"CSV Data Dates:\n{csv_data.index}")
        print(f"Fetched Data Dates:\n{fetched_data.index}")
        return

    # Compare the adjusted close prices (rounding to 2 decimal places for tolerance)
    for ticker in tickers:
        if ticker in csv_data.columns:
            if (csv_data[ticker].round(2) == fetched_data[ticker].round(2)).all():
                print(f"{ticker}: The data matches successfully!")
            else:
                print(f"{ticker}: Data mismatch detected!")
                print(f"CSV Data for {ticker}:\n{csv_data[ticker].head()}")
                print(f"Fetched Data for {ticker}:\n{fetched_data[ticker].head()}")

# Main script to download, load, and compare
if __name__ == "__main__":
    print("Starting the test...")

    tickers = ['AAPL', 'GOOGL']  # Example tickers to test

    # Step 1: Download data and save to CSV
    data = fetch_real_data(tickers=['AAPL', 'GOOGL'], start_date="2021-05-12", end_date="2022-05-12")

    # Step 2: Compare downloaded CSV with fetched data
    compare_data("AAPL_GOOGL_data.csv", tickers, start_date="2021-05-12", end_date="2022-05-12")

    print("Test completed.")