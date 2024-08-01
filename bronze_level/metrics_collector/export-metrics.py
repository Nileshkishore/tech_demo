import psycopg2
from prometheus_client import Gauge, start_http_server
import time
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database connection details (using environment variables for better security)
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'first_database')
DB_USER = os.getenv('DB_USER', 'postgres_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1234')

# Define Prometheus metrics
metric_current = Gauge('stock_current_price', 'Current stock price', ['symbol'])
metric_today_open = Gauge('stock_today_open', 'Stock price at market open today', ['symbol'])
metric_today_high = Gauge('stock_today_high', 'Stock highest price today', ['symbol'])
metric_today_low = Gauge('stock_today_low', 'Stock lowest price today', ['symbol'])
metric_weekly_high = Gauge('stock_weekly_high', 'Weekly highest stock price', ['symbol'])
metric_weekly_low = Gauge('stock_weekly_low', 'Weekly lowest stock price', ['symbol'])
metric_monthly_high = Gauge('stock_monthly_high', 'Monthly highest stock price', ['symbol'])
metric_monthly_low = Gauge('stock_monthly_low', 'Monthly lowest stock price', ['symbol'])
metric_yearly_high = Gauge('stock_yearly_high', 'Yearly highest stock price', ['symbol'])
metric_yearly_low = Gauge('stock_yearly_low', 'Yearly lowest stock price', ['symbol'])
metric_today_change = Gauge('stock_today_change', 'Change in stock price today', ['symbol'])
metric_week_change = Gauge('stock_week_change', 'Change in stock price over the week', ['symbol'])
metric_month_change = Gauge('stock_month_change', 'Change in stock price over the month', ['symbol'])
metric_year_change = Gauge('stock_year_change', 'Change in stock price over the year', ['symbol'])

def fetch_data_from_postgres():
    """Fetch stock data from PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT "Symbol", "Current", "Today_Open", "Today_High", "Today_Low", 
                   "Weekly_High", "Weekly_Low", "Monthly_High", "Monthly_Low", 
                   "Yearly_High", "Yearly_Low", "Today_Change", "1_Week_Change", 
                   "1_Month_Change", "1_Year_Change"
            FROM company_data_test;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        logging.error(f"Error fetching data from PostgreSQL: {e}")
        return []

def collect_metrics():
    """Collect metrics from the PostgreSQL database and expose them to Prometheus."""
    stock_data = fetch_data_from_postgres()
    
    for row in stock_data:
        symbol = row[0]
        try:
            metric_current.labels(symbol=symbol).set(row[1])
            metric_today_open.labels(symbol=symbol).set(row[2])
            metric_today_high.labels(symbol=symbol).set(row[3])
            metric_today_low.labels(symbol=symbol).set(row[4])
            metric_weekly_high.labels(symbol=symbol).set(row[5])
            metric_weekly_low.labels(symbol=symbol).set(row[6])
            metric_monthly_high.labels(symbol=symbol).set(row[7])
            metric_monthly_low.labels(symbol=symbol).set(row[8])
            metric_yearly_high.labels(symbol=symbol).set(row[9])
            metric_yearly_low.labels(symbol=symbol).set(row[10])
            metric_today_change.labels(symbol=symbol).set(row[11])
            metric_week_change.labels(symbol=symbol).set(row[12])
            metric_month_change.labels(symbol=symbol).set(row[13])
            metric_year_change.labels(symbol=symbol).set(row[14])
        except Exception as e:
            logging.error(f"Error setting metric for symbol {symbol}: {e}")

if __name__ == '__main__':
    # Start the Prometheus metrics server
    start_http_server(7878)  
    logging.info("Prometheus metrics server started on port 7878")

    # Main loop to update metrics periodically
    while True:
        collect_metrics()
        time.sleep(60)  # Collect data every 60 seconds

