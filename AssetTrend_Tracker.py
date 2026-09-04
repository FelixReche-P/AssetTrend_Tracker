import pandas as pd
import requests
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Extract with public API, with default values
def fetch_crypto_data(symbol="BTCUSDT", interval="1m", limit=1000):
    # Builds a URL with parameters including API key
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    
    # Sends GET request to the API.
    response = requests.get(url)
    response.raise_for_status() # status code to confirm request success (200 means OK).
    
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 
               'close_time', 'quote_asset_volume', 'trades', 
               'taker_buy_base', 'taker_buy_quote', 'ignore']
    
    df = pd.DataFrame(response.json(), columns=columns)
    
    # Transform, clean data
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    cols_to_keep = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df = df[cols_to_keep].astype({
        'open': 'float', 'high': 'float', 'low': 'float', 
        'close': 'float', 'volume': 'float'
    })
    
    return df

# Load to MySQL
def batch_insert_market_data(df, asset_id, db_config):
    records_to_insert = []
    for row in df.itertuples(index=False):
        records_to_insert.append((
            asset_id, 
            row.timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
            row.open, row.high, row.low, row.close, row.volume
        ))

    # Initialize the variables to prevent the UnboundLocalError if connection fails
    connection = None
    cursor = None

    
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Use INSERT IGNORE so that the script is safe and doesn't duplicate
            sql_insert_query = """
                INSERT IGNORE INTO market_data 
                (asset_id, timestamp, open, high, low, close, volume) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(sql_insert_query, records_to_insert)
            connection.commit()
            
            print(f"Success: {cursor.rowcount} new records inserted out of {len(records_to_insert)} processed.")
            
    except Error as e:
        print(f"Error connecting or inserting into MySQL: {e}")
    finally:
        # Safe closing of the connections
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

# Main Execution
if __name__ == "__main__":
    DB_CONFIG = {
        'host': 'localhost',
        'database': 'assettrend_tracker',
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS')
    }
    
    # Dictionary with the 3 coins and their corresponding IDs in the database
    coins_to_download = {
        1: "BTCUSDT", # Bitcoin
        2: "ETHUSDT", # Ethereum
        3: "SOLUSDT"  # Solana
    }
    
    print("Starting multi-asset pipeline")
    
    # Iterate over the dictionary to process all coins
    for asset_id, symbol in coins_to_download.items():
        print(f"\nDownloading data for {symbol}")
        df_market_data = fetch_crypto_data(symbol=symbol, interval="1m", limit=1000)
        
        print(f"Inserting into the database for ID {asset_id}")
        batch_insert_market_data(df_market_data, asset_id, DB_CONFIG)
        
    print("\nPipeline finished successfully!")