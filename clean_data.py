import pandas as pd
import os
import shutil
import glob

RAW_DIR = "data/raw"
PROC_DIR = "data/processed"

def clean_nav_history():
    print("Cleaning nav_history...")
    df = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
    
    # Parse dates
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    
    # Validate NAV > 0
    df = df[df['nav'] > 0]
    
    # Forward-fill missing dates for each amfi_code
    # Group by amfi_code, reindex to daily, ffill
    min_date = df['date'].min()
    max_date = df['date'].max()
    all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
    
    df = df.set_index('date')
    df_clean = df.groupby('amfi_code')['nav'].apply(
        lambda x: x.reindex(all_dates).ffill()
    ).reset_index()
    
    df_clean.rename(columns={'level_1': 'date'}, inplace=True)
    df_clean['date'] = df_clean['date'].dt.strftime('%Y-%m-%d')
    
    df_clean.to_csv(os.path.join(PROC_DIR, "02_nav_history.csv"), index=False)
    print(f"nav_history cleaned: {len(df_clean)} rows.")

def clean_investor_transactions():
    print("Cleaning investor_transactions...")
    df = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"))
    
    # Parse dates
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
    
    # Validate amount > 0
    df = df[df['amount_inr'] > 0]
    
    # Standardize transaction types
    df['transaction_type'] = df['transaction_type'].str.title().str.strip()
    
    # Filter valid KYC statuses
    df = df[df['kyc_status'].isin(['Verified', 'Pending'])]
    
    df.to_csv(os.path.join(PROC_DIR, "08_investor_transactions.csv"), index=False)
    print(f"investor_transactions cleaned: {len(df)} rows.")

def clean_scheme_performance():
    print("Cleaning scheme_performance...")
    df = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))
    
    # Return values should be numeric, coerce errors
    num_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Filter valid expense ratios (0.1 to 2.5)
    df = df[(df['expense_ratio_pct'] >= 0.1) & (df['expense_ratio_pct'] <= 2.5)]
    
    df.to_csv(os.path.join(PROC_DIR, "07_scheme_performance.csv"), index=False)
    print(f"scheme_performance cleaned: {len(df)} rows.")

def process_other_files():
    all_raw = set(os.path.basename(f) for f in glob.glob(os.path.join(RAW_DIR, "*.csv")))
    cleaned = {'02_nav_history.csv', '08_investor_transactions.csv', '07_scheme_performance.csv'}
    to_copy = all_raw - cleaned
    
    for f in to_copy:
        shutil.copy(os.path.join(RAW_DIR, f), os.path.join(PROC_DIR, f))
        print(f"Copied {f} to processed.")

if __name__ == "__main__":
    os.makedirs(PROC_DIR, exist_ok=True)
    clean_nav_history()
    clean_investor_transactions()
    clean_scheme_performance()
    process_other_files()
    print("--- Data Cleaning Complete ---")
