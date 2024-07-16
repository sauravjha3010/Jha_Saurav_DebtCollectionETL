# Debt Collection ETL and Basic Analysis

## Overview
This project performs a basic ETL (Extract, Transform, Load) process on a CSV file containing borrower data, loads it into an SQLite database, and conducts simple analysis for debt collection purposes.

## Requirements
- Python 3.x
- pandas library
- SQLite

## Files
- `etl_script.py`: Python script for the ETL process
- `analysis_queries.sql`: SQL script containing the queries for the basic analysis
- `analysis_results.txt`: Text file with the results of the analysis
- `README.md`: This file with instructions and details

## Instructions
1. Ensure you have Python and the required libraries installed.
2. Place the `5k_borrowers_data.csv` file in the same directory as `etl_script.py`.
3. Run the `etl_script.py` script:
4. The script will extract, transform, and load the data into an SQLite database (`debt_collection.db`), and perform the analysis.
5. The results of the analysis will be written to `analysis_results.txt`.

## Analysis Queries
The SQL queries used for analysis can be found in `analysis_queries.sql`.

## Contact
For any questions or issues, please contact [sauravjha62@gmail.com].
