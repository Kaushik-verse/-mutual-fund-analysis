import pandas as pd
import sqlite3
import sys

def get_recommendations(risk_appetite):
    """
    Recommends top 3 funds by Sharpe ratio matching the given risk appetite.
    risk_appetite: 'Low', 'Moderate', or 'High'
    """
    risk_appetite = risk_appetite.title()
    if risk_appetite not in ['Low', 'Moderate', 'High']:
        print("Invalid risk appetite. Please choose from: Low, Moderate, High")
        return
        
    import pathlib
    db_path = pathlib.Path(__file__).parent.parent / "data/db/bluestock_mf.db"
    conn = sqlite3.connect(db_path)
    
    # Map user risk appetite to SEBI risk categories roughly
    risk_mapping = {
        'Low': "('Low', 'Low to Moderate')",
        'Moderate': "('Moderate', 'Moderately High')",
        'High': "('High', 'Very High')"
    }
    
    query = f"""
    SELECT 
        f.amfi_code,
        f.scheme_name,
        f.fund_house,
        f.category,
        f.risk_category,
        p.sharpe_ratio,
        p.return_3yr_pct
    FROM dim_fund f
    JOIN fact_performance p ON f.amfi_code = p.amfi_code
    WHERE f.risk_category IN {risk_mapping[risk_appetite]}
      AND p.sharpe_ratio IS NOT NULL
    ORDER BY p.sharpe_ratio DESC
    LIMIT 3
    """
    
    try:
        df_reco = pd.read_sql(query, conn)
    except Exception as e:
        print(f"Error executing query: {e}")
        return
    finally:
        conn.close()
        
    if df_reco.empty:
        print(f"No funds found for risk appetite: {risk_appetite}")
        return
        
    print(f"\n{'='*60}")
    print(f"TOP 3 FUND RECOMMENDATIONS (Risk: {risk_appetite})")
    print(f"{'='*60}")
    
    for idx, row in df_reco.iterrows():
        print(f"{idx+1}. {row['scheme_name']}")
        print(f"   Category: {row['category']} | Fund House: {row['fund_house']}")
        print(f"   Sharpe Ratio: {row['sharpe_ratio']:.2f} | 3Yr Return: {row['return_3yr_pct']:.2f}%")
        print(f"   SEBI Risk: {row['risk_category']}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        appetite = sys.argv[1]
    else:
        appetite = input("Enter your risk appetite (Low / Moderate / High): ")
    
    get_recommendations(appetite)
