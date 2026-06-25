import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

DB_PATH = "bluestock_mf.db"
PROC_DIR = "data/processed"

def init_db():
    print("Initializing Database with schema.sql...")
    conn = sqlite3.connect(DB_PATH)
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
    conn.close()

def load_data():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    
    file_mapping = {
        "01_fund_master.csv": "dim_fund",
        "02_nav_history.csv": "fact_nav",
        "03_aum_by_fund_house.csv": "fact_aum",
        "04_monthly_sip_inflows.csv": "fact_sip_industry",
        "07_scheme_performance.csv": "fact_performance",
        "08_investor_transactions.csv": "fact_transactions",
        "09_portfolio_holdings.csv": "fact_portfolio",
    }
    
    for filename, table_name in file_mapping.items():
        filepath = os.path.join(PROC_DIR, filename)
        if os.path.exists(filepath):
            print(f"Loading {filename} into {table_name}...")
            df = pd.read_csv(filepath)
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"  Loaded {len(df)} rows.")
        else:
            print(f"Warning: {filepath} not found.")

    # Generate dim_date dynamically
    print("Generating dim_date...")
    dates = pd.date_range(start='2022-01-01', end='2026-12-31')
    dim_date = pd.DataFrame({
        'date_id': range(1, len(dates) + 1),
        'date': dates.strftime('%Y-%m-%d'),
        'year': dates.year,
        'month': dates.month,
        'quarter': dates.quarter,
        'is_weekday': dates.weekday < 5
    })
    dim_date.to_sql('dim_date', engine, if_exists='replace', index=False)
    print(f"  Loaded {len(dim_date)} rows.")

    # Load benchmarks
    filepath = os.path.join(PROC_DIR, "10_benchmark_indices.csv")
    if os.path.exists(filepath):
        print(f"Loading 10_benchmark_indices.csv into fact_benchmark...")
        df = pd.read_csv(filepath)
        df.to_sql('fact_benchmark', engine, if_exists='replace', index=False)
        print(f"  Loaded {len(df)} rows.")

def verify_counts():
    print("\n--- Row Count Verification ---")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        tname = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {tname}")
        count = cursor.fetchone()[0]
        print(f"Table '{tname}': {count} rows")
    conn.close()

if __name__ == "__main__":
    init_db()
    load_data()
    verify_counts()
    print("--- Database Load Complete ---")
