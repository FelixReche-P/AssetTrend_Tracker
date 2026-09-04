# AssetTrend Tracker: End-to-End Crypto ETL Pipeline 

Hi! Welcome to my first data project. This is a robust data pipeline I built to extract real-time financial market data, transform it into a structured format, and store it in a relational database for future predictive analysis and visualization.

## Architecture & Technologies
* Extraction (API): Consumes the public Binance API using Python's `requests` library.
* Transformation: Handles data cleaning, strict typing, and timestamp formatting using `pandas`.
* Loading (Database): Automated data insertion into a local MySQL database using the native Python connector.
* Visualization: Direct connection and data modeling built in Power BI.

## Decisions: Why I built it this way
* Fault Tolerance: Implemented composite keys `UNIQUE KEY` and `INSERT IGNORE` clauses to ensure that network drops or duplicate runs don't corrupt the database.
* Strict Relational Modeling: Designed a database schema that separates static data from transactional data (`market_data` and `model_predictions`) using proper foreign keys.
* Financial Precision: Used the `DECIMAL(18,8)` data type in SQL to avoid classic floating-point rounding errors when dealing with crypto prices.

## Setup Instructions

If you want to run this pipeline on your local machine, follow these steps:

## Clone the repository
Open your terminal and run:
```bash
git clone [https://github.com/FelixReche-P/AssetTrend_Tracker.git](https://github.com/FelixReche-P/AssetTrend_Tracker.git) 
cd AssetTrend_Tracker
```

## Install dependences
You need to have Python, then install the required libraries:
pip install pandas requests mysql-connector-python

## Set up the Database
Run the included database_schema.sql script in your MySQL manager to generate the assettrend_track database structure and tables.

## Configure your credentials
Create a new text file in the main folder named exactly credentials.env. Add your MySQL database connection details inside (user, password). This file is protected by .gitignore.

## Run the pipeline
Execute the main script to start ingesting data:
python AssetTrend_Tracker.py
