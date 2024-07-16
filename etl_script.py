import pandas as pd
import sqlite3
from datetime import datetime

# 1. Data Extraction
def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print(f"Data extracted successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

# 2. Data Transformation
def transform_data(df):
    # Clean and standardize data
    df['Phone Number'] = df['Phone Number'].astype(str).str.replace(r'\D', '', regex=True)
    df['Loan Amount'] = pd.to_numeric(df['Loan Amount'], errors='coerce')
    df['Interest Rate'] = pd.to_numeric(df['Interest Rate'], errors='coerce')
    df['Days Left to Pay Current EMI'] = pd.to_numeric(df['Days Left to Pay Current EMI'], errors='coerce')
    
    # Convert 'Date of Birth' to datetime
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'], format='%d-%m-%Y', errors='coerce')
    
    print("Data transformed successfully")
    return df

# 3. Data Loading
def load_data(df, db_name):
    conn = sqlite3.connect(db_name)
    
    # Create table
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS borrowers (
        Name TEXT,
        "Date of Birth" TEXT,
        Gender TEXT,
        "Marital Status" TEXT,
        "Phone Number" TEXT,
        "Email Address" TEXT,
        "Mailing Address" TEXT,
        "Language Preference" TEXT,
        "Geographical Location" TEXT,
        "Credit Score" INTEGER,
        "Loan Type" TEXT,
        "Loan Amount" REAL,
        "Loan Term" INTEGER,
        "Interest Rate" REAL,
        "Loan Purpose" TEXT,
        EMI REAL,
        "IP Address" TEXT,
        Geolocation TEXT,
        "Repayment History" TEXT,
        "Days Left to Pay Current EMI" INTEGER,
        "Delayed Payment" TEXT
    )
    '''
    conn.execute(create_table_query)
    
    # Insert data
    df.to_sql('borrowers', conn, if_exists='replace', index=False)
    
    print(f"Data loaded successfully into {db_name}")
    conn.close()

# 4. Basic Analysis
def perform_analysis(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # a. Average loan amount for borrowers who are more than 5 days past due
    query_a = '''
    SELECT AVG([Loan Amount]) as average_loan_amount
    FROM borrowers
    WHERE [Days Left to Pay Current EMI] <= 5
    '''
    cursor.execute(query_a)
    result_a = cursor.fetchone()[0]
    print("Query A result:", result_a)
    
    # b. Top 10 borrowers with the highest outstanding balance
    query_b = '''
    SELECT Name, [Loan Amount] 
    FROM borrowers 
    ORDER BY [Loan Amount] DESC 
    LIMIT 10
    '''
    cursor.execute(query_b)
    result_b = cursor.fetchall()
    print("Query B result:", result_b)
    
    # c. List of all borrowers with good repayment history
    query_c = '''
    SELECT Name 
    FROM borrowers 
    WHERE [Delayed Payment] = 'No'
    '''
    cursor.execute(query_c)
    result_c = cursor.fetchall()
    print("Query C result:", result_c[:5])  # Print first 5 results
    
    # d. Brief analysis with respect to loan type
    query_d = '''
    SELECT [Loan Type], 
           COUNT(*) as Count, 
           AVG([Loan Amount]) as Avg_Loan_Amount,
           AVG([Interest Rate]) as Avg_Interest_Rate
    FROM borrowers 
    GROUP BY [Loan Type]
    '''
    cursor.execute(query_d)
    result_d = cursor.fetchall()
    print("Query D result:", result_d)
    
    conn.close()
    
    return result_a, result_b, result_c, result_d

# Main execution
if __name__ == "__main__":
    file_path = "/content/5k_borrowers_data.csv"  # Replace with your actual file path
    db_name = "debt_collection.db"
    
    # ETL Process
    df = extract_data(file_path)
    if df is not None:
        df_transformed = transform_data(df)
        load_data(df_transformed, db_name)
        
        # Analysis
        result_a, result_b, result_c, result_d = perform_analysis(db_name)
        
        # Write results to file
        with open("analysis_results.txt", "w") as f:
            f.write("a. Average loan amount for borrowers who are more than 5 days past due:\n")
            if result_a is not None:
                f.write(f"{result_a:.2f}\n\n")
            else:
                f.write("No borrowers are more than 5 days past due.\n\n")
            
            f.write("b. Top 10 borrowers with the highest outstanding balance:\n")
            for name, amount in result_b:
                f.write(f"{name}: {amount:.2f}\n")
            f.write("\n")
            
            f.write("c. List of borrowers with good repayment history:\n")
            for (name,) in result_c:
                f.write(f"{name}\n")
            f.write("\n")
            
            f.write("d. Brief analysis with respect to loan type:\n")
            for loan_type, count, avg_amount, avg_rate in result_d:
                f.write(f"Loan Type: {loan_type}\n")
                f.write(f"Count: {count}\n")
                f.write(f"Average Loan Amount: {avg_amount:.2f}\n")
                f.write(f"Average Interest Rate: {avg_rate:.2f}\n\n")
        
        print("Analysis complete. Results written to analysis_results.txt")
