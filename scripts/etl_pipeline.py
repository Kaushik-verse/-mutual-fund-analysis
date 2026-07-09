"""
etl_pipeline.py — Step 1: Data Ingestion.

Discovers and copies all CSV datasets from the source directory
into the project's data/raw/ staging area, then prints a summary
of each file's shape, data types, and first two rows for validation.

Author: Kaushik
"""

import pandas as pd
import glob
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = "/Users/manivannan/Downloads/bluestock_mf_datasets"
DEST_DIR = BASE_DIR / "data/raw"


def ingest_data():
    """Copy all CSV files from SOURCE_DIR into the project raw data folder."""
    print(f"Ingesting datasets from {SOURCE_DIR} to {DEST_DIR}...")
    os.makedirs(DEST_DIR, exist_ok=True)
    
    csv_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.csv")))
    if not csv_files:
        print(f"No CSV files found in {SOURCE_DIR}")
        return
        
    for file_path in csv_files:
        filename = os.path.basename(file_path)
        dest_path = os.path.join(DEST_DIR, filename)
        shutil.copy(file_path, dest_path)
        print(f"Copied {filename}")
        
    print("\n--- Data Ingestion Complete ---")

def explore_data():
    print("--- Exploring Ingested Datasets ---")
    raw_files = sorted(glob.glob(os.path.join(DEST_DIR, "*.csv")))
    
    for file_path in raw_files:
        filename = os.path.basename(file_path)
        print(f"\n[{filename}]")
        try:
            df = pd.read_csv(file_path)
            print(f"Shape: {df.shape}")
            print("Data Types:")
            print(df.dtypes)
            print("Head:")
            print(df.head(2))
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    ingest_data()
    explore_data()
