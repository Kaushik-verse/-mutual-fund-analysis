import pandas as pd
import numpy as np
import os

def clean_data():
    os.makedirs('data/processed', exist_ok=True)
    
    # 1. nav_history.csv
    print("Cleaning nav_history.csv...")
    nav = pd.read_csv('data/raw/nav_history.csv')
    nav['date'] = pd.to_datetime(nav['date'], format='%d-%m-%Y', errors='coerce')
    nav = nav.dropna(subset=['date'])
    nav['nav'] = pd.to_numeric(nav['nav'], errors='coerce')
    nav = nav[nav['nav'] > 0] # validate NAV > 0
    nav = nav.drop_duplicates(subset=['scheme_code', 'date'])
    nav = nav.sort_values(by=['scheme_code', 'date'])
    
    # forward-fill missing NAV for holidays/weekends
    # Create a complete date range per scheme code
    all_dates = pd.date_range(start=nav['date'].min(), end=nav['date'].max(), freq='D')
    nav_filled = []
    for code, group in nav.groupby('scheme_code'):
        group = group.set_index('date').reindex(all_dates)
        group['scheme_code'] = code
        group['nav'] = group['nav'].ffill()
        group = group.dropna(subset=['nav'])
        group = group.reset_index().rename(columns={'index': 'date'})
        nav_filled.append(group)
    nav_clean = pd.concat(nav_filled, ignore_index=True)
    nav_clean.to_csv('data/processed/nav_history.csv', index=False)
    
    # 2. investor_transactions.csv
    print("Cleaning investor_transactions.csv...")
    txn = pd.read_csv('data/raw/investor_transactions.csv')
    # Standardise transaction_type
    txn['transaction_type'] = txn['transaction_type'].str.upper().replace({'LUMP': 'LUMPSUM'})
    valid_txns = ['SIP', 'LUMPSUM', 'REDEMPTION']
    txn = txn[txn['transaction_type'].isin(valid_txns)]
    # Validate amount > 0
    txn = txn[txn['amount'] > 0]
    # Fix date formats
    txn['date'] = pd.to_datetime(txn['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    txn = txn.dropna(subset=['date'])
    # KYC status enum values
    txn['kyc_status'] = txn['kyc_status'].str.upper()
    valid_kyc = ['VERIFIED', 'PENDING', 'REJECTED']
    txn = txn[txn['kyc_status'].isin(valid_kyc)]
    txn.to_csv('data/processed/investor_transactions.csv', index=False)
    
    # 3. scheme_performance.csv
    print("Cleaning scheme_performance.csv...")
    perf = pd.read_csv('data/raw/scheme_performance.csv')
    perf['1y_return'] = pd.to_numeric(perf['1y_return'], errors='coerce')
    perf['3y_return'] = pd.to_numeric(perf['3y_return'], errors='coerce')
    perf['5y_return'] = pd.to_numeric(perf['5y_return'], errors='coerce')
    
    # Flag anomalies > 100%
    perf['is_anomaly'] = (perf['1y_return'] > 100) | (perf['3y_return'] > 100) | (perf['5y_return'] > 100)
    
    # Check expense_ratio range (0.1% - 2.5%)
    perf = perf[(perf['expense_ratio'] >= 0.1) & (perf['expense_ratio'] <= 2.5)]
    perf.to_csv('data/processed/scheme_performance.csv', index=False)
    
    # Pass-through other datasets to processed
    print("Processing other datasets...")
    for filename in ['fund_master.csv', 'aum.csv', 'investors.csv', 'distributors.csv', 'market_indices.csv', 'fund_managers.csv', 'dividends.csv']:
        df = pd.read_csv(f'data/raw/{filename}')
        df.to_csv(f'data/processed/{filename}', index=False)
        
if __name__ == "__main__":
    clean_data()
    print("Data cleaning complete.")
