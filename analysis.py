import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Reuse connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'assettrend_tracker',
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS')
}

def extract_market_data():
    try:
        # Open connection
        connection = mysql.connector.connect(**DB_CONFIG)
        
        # Write a SQL query (JOIN)
        # Fetch the coin symbol, date, close price, and volume.
        query = """
            SELECT 
                a.symbol, 
                m.timestamp, 
                m.close, 
                m.volume
            FROM market_data m
            INNER JOIN assets a ON m.asset_id = a.id
            ORDER BY m.timestamp DESC
        """
        
        # Pandas executes the query and automatically converts everything into a DataFrame
        df = pd.read_sql(query, connection)
        
        return df

    except Exception as e:
        print(f"Error extracting data: {e}")
    finally:
        # Always close the connection
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# === Main Execution ===
if __name__ == "__main__":
    print("Extracting data from MySQL")
    df_analysis = extract_market_data()
    
    if df_analysis is not None and not df_analysis.empty:
        print(f"Success! {len(df_analysis)} records loaded into memory.")
        
        # Show the first 5 rows to check that everything is fine
        print("\nData sample:")
        print(df_analysis.head())
        
    else:
        print("No data found.")