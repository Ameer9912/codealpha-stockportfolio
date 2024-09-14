import requests
import pandas as pd
import matplotlib.pyplot as plt

# Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
API_KEY = ' 54C136VDHGNXBGKP'
BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_data(symbol):
    """Fetch stock data from Alpha Vantage."""
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if 'Time Series (Daily)' not in data:
        print(f"Error fetching data for {symbol}: {data.get('Error Message', 'Unknown error')}")
        return None
    return pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')

def plot_stock_data(df, symbol):
    """Plot stock data."""
    df.index = pd.to_datetime(df.index)
    df['4. close'] = pd.to_numeric(df['4. close'])
    df['4. close'].plot(title=f"Stock Prices for {symbol}")
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.show()

def add_stock(portfolio, symbol, shares):
    """Add a stock to the portfolio."""
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares
    print(f"Added {shares} shares of {symbol} to the portfolio.")

def remove_stock(portfolio, symbol, shares):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        if portfolio[symbol] <= shares:
            del portfolio[symbol]
            print(f"Removed all shares of {symbol} from the portfolio.")
        else:
            portfolio[symbol] -= shares
            print(f"Removed {shares} shares of {symbol} from the portfolio.")
    else:
        print(f"No shares of {symbol} found in the portfolio.")

def print_portfolio(portfolio):
    """Print the current portfolio."""
    print("Current Portfolio:")
    for symbol, shares in portfolio.items():
        print(f"{symbol}: {shares} shares")

def main():
    portfolio = {}
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add stock")
        print("2. Remove stock")
        print("3. View portfolio")
        print("4. View stock data")
        print("5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ")
            shares = int(input("Enter number of shares: "))
            add_stock(portfolio, symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol: ")
            shares = int(input("Enter number of shares: "))
            remove_stock(portfolio, symbol, shares)
        elif choice == '3':
            print_portfolio(portfolio)
        elif choice == '4':
            symbol = input("Enter stock symbol: ")
            df = get_stock_data(symbol)
            if df is not None:
                plot_stock_data(df, symbol)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
