# Bluestock Mutual Fund Analytics Platform

**Author:** Kaushik

This repository contains the codebase for an end-to-end data engineering, ETL, and analytics capstone project focused on the Indian Mutual Fund industry. It ingests official AMFI (Association of Mutual Funds in India) datasets, processes them into a normalized SQLite Star Schema, and performs comprehensive exploratory data analysis (EDA).

## Project Overview

Despite the massive growth of India's mutual fund industry (managing over ₹81 lakh crore in AUM), investors often struggle to make data-driven fund selection decisions due to fragmented data. This project solves this by:
1. Consolidating fragmented data (NAV, AUM, SIP flows, Portfolio Holdings) into a single SQLite database.
2. Cleaning and standardizing the data.
3. Providing deep analytical insights and visualizations regarding fund performance, investor demographics, and macro-industry trends.

## Datasets

The project utilizes 10 core datasets containing simulated but highly realistic Indian mutual fund data (anchored to true historical NAVs and AUMs):
1. **Fund Master**: Scheme metadata (Category, Benchmark, Expense Ratio).
2. **NAV History**: Daily NAVs for 40 real schemes (Jan 2022 - May 2026).
3. **AUM by Fund House**: Quarterly AUM totals for top AMCs.
4. **Monthly SIP Inflows**: Macro industry SIP volume and AUM.
5. **Category Inflows**: Net inflows by fund category (Large Cap, Mid Cap, etc.).
6. **Industry Folio Count**: Growth of investor accounts (folios).
7. **Scheme Performance**: Trailing returns, Alpha, Beta, Sharpe, and Drawdowns.
8. **Investor Transactions**: Over 32,000 simulated transactions with geographic and demographic data.
9. **Portfolio Holdings**: Equity sector allocations and stock weights.
10. **Benchmark Indices**: Daily closing values for Nifty 50, Nifty 100, etc.

## Project Structure

```
.
├── data/
│   ├── raw/               # Original CSV files ingested during Day 1
│   └── processed/         # Cleaned, standardized CSVs ready for DB load
├── notebooks/
│   ├── EDA_Analysis.ipynb         # 10+ Plotly/Seaborn charts
│   └── Performance_Analytics.ipynb# Risk models and Fund Scorecards
│   └── Advanced_Analytics.ipynb   # VaR, Cohort Analysis, HHI
├── reports/
│   ├── charts/                    # PNG exports of all visualizations
│   └── data/                      # CSV exports (scorecard, var, etc.)
├── dashboard/
│   └── app.py                     # Streamlit Interactive Dashboard
├── sql/
│   ├── schema.sql                 # DDL statements for the 5-table Star Schema
│   └── queries.sql                # 10 complex analytical SQL queries
├── data_ingestion.py              # Script to ingest raw datasets
├── clean_data.py                  # ETL script to clean datasets
├── db_load.py                     # SQLAlchemy script to map processed CSVs to SQLite
├── generate_day4.py               # Notebook generator for Day 4
├── generate_day6.py               # Notebook generator for Day 6
├── recommender.py                 # CLI Fund Recommender
├── data_dictionary.md             # Database schema documentation
└── requirements.txt               # Python dependencies
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kaushik-verse/-mutual-fund-analysis.git
   cd -mutual-fund-analysis
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Execution Workflow

1. **Day 1: Data Ingestion**
   ```bash
   python data_ingestion.py
   ```
   *Copies source datasets into `data/raw/`.*

2. **Day 2: Data Cleaning & Database Load**
   ```bash
   python clean_data.py
   python db_load.py
   ```
   *Cleans the raw data and builds the `bluestock_mf.db` SQLite database.*

3. **Day 2: SQL Analytics**
   ```bash
   sqlite3 bluestock_mf.db < queries.sql
   ```
   *Executes pre-built analytical queries against the Star Schema.*

4. **Day 3: Exploratory Data Analysis**
   Launch Jupyter Notebook to view the charts:
   ```bash
   jupyter notebook notebooks/EDA_Analysis.ipynb
   ```

5. **Day 4: Fund Performance Analytics**
   ```bash
   jupyter notebook notebooks/Performance_Analytics.ipynb
   ```

6. **Day 5: Interactive Dashboard Deployment**
   Launch the Streamlit web dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

7. **Day 6: Advanced Analytics & Models**
   ```bash
   jupyter notebook notebooks/Advanced_Analytics.ipynb
   ```
   Run the CLI Fund Recommender:
   ```bash
   python recommender.py
   ```

## Technologies Used
- **Language**: Python 3
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite3, SQLAlchemy
- **Visualisation**: Plotly, Seaborn, Matplotlib
- **Notebooks**: Jupyter Lab
- **Version Control**: Git & GitHub

---
*Disclaimer: All mutual fund NAVs and AUMs are based on publicly available AMFI data for educational purposes. Transactions are simulated for analytical demonstration. Mutual fund investments are subject to market risks.*
