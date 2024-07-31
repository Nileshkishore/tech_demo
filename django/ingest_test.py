import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine

# Function to get the last available trading day data
def get_last_available_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date, interval="1d")
    if not data.empty:
        return data.iloc[-1]  # Get the most recent entry
    return None

# List of company tickers
symbols = ["TCS.NS", "RELIANCE.NS", "INFY.NS", "HDFCBANK.NS","WIPRO.NS", "AAPL", "RR.L","STAN.L","MSFT"]

# List to store the data
data_list = []

for symbol in symbols:
    # Fetch stock data
    stock = yf.Ticker(symbol)
    
    # Automatically fetch company name and currency
    company_info = stock.info
    name = company_info.get("longName", "N/A")  # Use 'N/A' if company name is not available
    currency = company_info.get('currency', 'N/A')  # Automatically infer currency

    data = stock.history(period='1d')
    
    today = data.index[-1].date()  # Extract date object
    one_week_ago = today - timedelta(days=7)
    one_month_ago = today - timedelta(days=30)
    one_year_ago = today - timedelta(days=365)

    # Fetch data for the specific dates
    today_data = get_last_available_data(symbol, today - timedelta(days=1), today + timedelta(days=1))
    week_ago_data = get_last_available_data(symbol, one_week_ago - timedelta(days=3), one_week_ago + timedelta(days=3))
    month_ago_data = get_last_available_data(symbol, one_month_ago - timedelta(days=3), one_month_ago + timedelta(days=3))
    year_ago_data = get_last_available_data(symbol, one_year_ago - timedelta(days=3), one_year_ago + timedelta(days=3))

    # Fetch historical data for high and low values
    weekly_hist = stock.history(period='5d')
    weekly_low = round(float(weekly_hist['Low'].min()), 4) if not weekly_hist.empty else float('nan')
    weekly_high = round(float(weekly_hist['High'].max()), 4) if not weekly_hist.empty else float('nan')

    monthly_hist = stock.history(period='1mo')
    monthly_low = round(float(monthly_hist['Low'].min()), 4) if not monthly_hist.empty else float('nan')
    monthly_high = round(float(monthly_hist['High'].max()), 4) if not monthly_hist.empty else float('nan')

    yearly_hist = stock.history(period='1y')
    yearly_low = round(float(yearly_hist['Low'].min()), 4) if not yearly_hist.empty else float('nan')
    yearly_high = round(float(yearly_hist['High'].max()), 4) if not yearly_hist.empty else float('nan')

    # Today's high, low, and opening price
    today_high = today_data['High'] if today_data is not None else float('nan')
    today_low = today_data['Low'] if today_data is not None else float('nan')
    today_open = today_data['Open'] if today_data is not None else float('nan')

    # Ensure data is not empty
    if today_data is not None and week_ago_data is not None and month_ago_data is not None and year_ago_data is not None:
        # Use the last available data if exact date is not available
        today_close = today_data['Close']
        week_ago_open = week_ago_data['Open']
        month_ago_open = month_ago_data['Open']
        year_ago_open = year_ago_data['Open']

        # Calculate percentage changes
        change_24h = ((today_close - today_open) / today_open) * 100
        change_1w = ((today_close - week_ago_open) / week_ago_open) * 100
        change_1m = ((today_close - month_ago_open) / month_ago_open) * 100
        change_1y = ((today_close - year_ago_open) / year_ago_open) * 100

        # Append to data list
        data_list.append([
            symbol, name, today_close, today, currency,
            today_open, change_24h, change_1w, change_1m, change_1y,
            week_ago_data.name.date(), month_ago_data.name.date(), year_ago_data.name.date(),
            today_high, today_low, weekly_low, weekly_high, monthly_low, monthly_high, yearly_low, yearly_high
        ])
    else:
        print(f"No data available for {symbol} on {today}, {one_week_ago}, {one_month_ago}, or {one_year_ago}")

# Create a DataFrame from the list
columns = ["Symbol", "Company_Name", "Current", "Current_Date", "Currency",
           "Today_Open", "Today_Change", "1_Week_Change", "1_Month_Change", "1_Year_Change",
           "1_Week_Back_Date", "1_Month_Back_Date", "1_Year_Back_Date",
           "Today_High", "Today_Low", "Weekly_Low", "Weekly_High", "Monthly_Low", "Monthly_High", "Yearly_Low", "Yearly_High"]
df = pd.DataFrame(data_list, columns=columns)

# Database connection parameters
db_params = {
    'dbname': 'first_database',
    'user': 'postgres_user',
    'password': '1234',
    'host': '127.0.0.1',
    'port': '5432'
}

# Create a connection string
conn_str = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"

# Create a SQLAlchemy engine
engine = create_engine(conn_str)

# Insert DataFrame into PostgreSQL table
df.to_sql('company_data_test', engine, if_exists='replace', index=False)

print("Data successfully inserted into PostgreSQL database.")
