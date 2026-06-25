import pandas as pd
import sqlite3
import os
from sqlalchemy import create_engine, text

def load_db():
    engine = create_engine('sqlite:///bluestock_mf.db')
    
    # 1. Run schema.sql first
    with sqlite3.connect('bluestock_mf.db') as conn:
        with open('schema.sql', 'r') as f:
            conn.executescript(f.read())
            
    print("Schema created successfully.")

    # 2. Load dimension: dim_fund
    fund_master = pd.read_csv('data/processed/fund_master.csv')
    fund_master.to_sql('dim_fund', engine, if_exists='append', index=False)
    
    # 3. Load facts
    # nav_history
    nav = pd.read_csv('data/processed/nav_history.csv')
    # Generate dim_date dynamically from all dates across datasets
    dates = pd.to_datetime(nav['date'].unique())
    txn = pd.read_csv('data/processed/investor_transactions.csv')
    dates = dates.union(pd.to_datetime(txn['date'].unique()))
    perf = pd.read_csv('data/processed/scheme_performance.csv')
    dates = dates.union(pd.to_datetime(perf['as_of_date'].unique()))
    aum = pd.read_csv('data/processed/aum.csv')
    dates = dates.union(pd.to_datetime(aum['as_of_date'].unique()))
    
    dim_date = pd.DataFrame({
        'date': dates.strftime('%Y-%m-%d'),
        'year': dates.year,
        'month': dates.month,
        'day': dates.day,
        'quarter': dates.quarter,
        'day_of_week': dates.dayofweek,
        'is_weekend': dates.dayofweek >= 5
    }).drop_duplicates()
    dim_date.to_sql('dim_date', engine, if_exists='append', index=False)
    
    nav.to_sql('fact_nav', engine, if_exists='append', index=False)
    
    txn.to_sql('fact_transactions', engine, if_exists='append', index=False)
    
    perf = perf.rename(columns={'1y_return': 'return_1y', '3y_return': 'return_3y', '5y_return': 'return_5y'})
    perf.to_sql('fact_performance', engine, if_exists='append', index=False)
    
    aum.to_sql('fact_aum', engine, if_exists='append', index=False)
    
    # other dims
    investors = pd.read_csv('data/processed/investors.csv')
    investors.to_sql('dim_investor', engine, if_exists='append', index=False)
    
    distributors = pd.read_csv('data/processed/distributors.csv')
    distributors.to_sql('dim_distributor', engine, if_exists='append', index=False)
    
    indices = pd.read_csv('data/processed/market_indices.csv')
    indices.to_sql('dim_market_index', engine, if_exists='append', index=False)
    
    mgrs = pd.read_csv('data/processed/fund_managers.csv')
    mgrs.to_sql('dim_fund_manager', engine, if_exists='append', index=False)
    
    divs = pd.read_csv('data/processed/dividends.csv')
    divs.to_sql('fact_dividend', engine, if_exists='append', index=False)
    
    # 4. Verify row counts
    print("\n--- Row Count Verification ---")
    tables = {
        'dim_fund': len(fund_master),
        'fact_nav': len(nav),
        'fact_transactions': len(txn),
        'fact_performance': len(perf),
        'fact_aum': len(aum),
        'dim_investor': len(investors),
        'dim_distributor': len(distributors),
        'dim_market_index': len(indices),
        'dim_fund_manager': len(mgrs),
        'fact_dividend': len(divs)
    }
    
    with engine.connect() as connection:
        for table, expected in tables.items():
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            status = "OK" if result == expected else f"MISMATCH (Expected: {expected}, Got: {result})"
            print(f"{table}: {status}")

if __name__ == "__main__":
    if os.path.exists('bluestock_mf.db'):
        os.remove('bluestock_mf.db')
    load_db()
    print("\nDatabase load complete.")
