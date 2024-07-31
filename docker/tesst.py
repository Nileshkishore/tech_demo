import yfinance as yf

def fetch_index_data(symbol):
    try:
        index = yf.Ticker(symbol)
        data = index.history(period='1d')
        if data.empty:
            raise ValueError("No data returned for symbol.")
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Define the symbols for the indices
symbols = {
    'Nifty 50': '^NSEI',
    'Dow Jones': '^DJI',
    # Add more symbols if needed
}

# Fetch and display data
for index_name, symbol in symbols.items():
    data = fetch_index_data(symbol)
    if data is not None:
        print(f"{index_name} ({symbol})")
        try:
            print("Current Price:", data['Close'].iloc[-1])
            print("High Price of the Day:", data['High'].iloc[-1])
            print("Low Price of the Day:", data['Low'].iloc[-1])
            print("Previous Close:", data['Close'].iloc[-2])
        except IndexError:
            print("Not enough data available.")
        print()
    else:
        print(f"Failed to retrieve data for {index_name} ({symbol})")
