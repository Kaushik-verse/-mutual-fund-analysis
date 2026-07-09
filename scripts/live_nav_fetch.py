"""
live_nav_fetch.py — Fetches real-time NAV data from mfapi.in REST API.

Used by the cron automation (schedule_cron.sh) to keep the database
synchronized with live market closes for 6 key large-cap schemes.

Author: Kaushik
"""

import pandas as pd
import requests
import os


def fetch_and_save_nav(scheme_code, filename):
    """Fetch live NAV for a given AMFI scheme code and save to CSV."""
    print(f"Fetching live NAV for scheme {scheme_code}...")
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Meta info
        meta = data.get("meta", {})
        scheme_name = meta.get("scheme_name", "Unknown")
        print(f"Scheme Name: {scheme_name}")
        
        # NAV history
        nav_data = data.get("data", [])
        if nav_data:
            df = pd.DataFrame(nav_data)
            df['scheme_code'] = scheme_code
            df['scheme_name'] = scheme_name
            
            # Print latest NAV
            latest = df.iloc[0]
            print(f"Latest NAV on {latest['date']}: {latest['nav']}\n")
            
            # Save to raw CSV
            filepath = os.path.join("data", "raw", filename)
            df.to_csv(filepath, index=False)
            print(f"Saved to {filepath}")
        else:
            print(f"No NAV data found for {scheme_code}")
    else:
        print(f"Failed to fetch data for {scheme_code}, Status code: {response.status_code}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    
    # Fetch HDFC Large Cap Direct Growth (Top 100 equivalent)
    fetch_and_save_nav(119018, "hdfc_large_cap_119018.csv")
    
    # Fetch 5 key schemes (Direct Growth versions)
    key_schemes = {
        "SBI Large Cap": 119598,
        "ICICI Large Cap": 120586,
        "Nippon Large Cap": 118632,
        "Axis Large Cap": 120465,
        "Kotak Large Cap": 120152
    }
    
    for name, code in key_schemes.items():
        fetch_and_save_nav(code, f"{name.replace(' ', '_').lower()}_{code}.csv")
