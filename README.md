# Bluestock Mutual Fund Analytics Platform

**Author:** Kaushik

A comprehensive, end-to-end data engineering, ETL, and quantitative analytics capstone project focused on the Indian Mutual Fund industry. It ingests 10 official AMFI datasets (580,000+ records), processes them into a normalized 5-table SQLite Star Schema, computes institutional-grade risk metrics, and delivers interactive visualizations through a Streamlit dashboard.

---

## Project Overview

The Indian mutual fund industry manages over INR 81 Lakh Crore in AUM across 1,900+ schemes and 26 Crore investor folios. Despite this massive scale, critical data remains fragmented across AMFI disclosures, AMC factsheets, and brokerage platforms. This project bridges that gap by:

1. **Automating data ingestion** of 10 heterogeneous CSV datasets into a staging layer.
2. **Cleaning and normalizing** data (forward-fill for missing NAV dates, deduplication, outlier removal).
3. **Loading into a Star Schema** SQLite database optimized for analytical queries.
4. **Computing 6 quantitative metrics** (CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown) for all 40 schemes.
5. **Advanced analytics** including VaR, CVaR, HHI concentration, investor cohort modeling, and SIP churn detection.
6. **Interactive Streamlit dashboard** with 4 pages, dynamic slicers, and Plotly visualizations.
7. **Bonus challenges** — Cron automation, Monte Carlo simulation, Markowitz optimization, automated email reports.

---

## Datasets

| # | File | Rows | Description |
|---|------|------|-------------|
| 1 | `01_fund_master.csv` | 40 | Scheme metadata, category, benchmark, expense ratio, risk grade |
| 2 | `02_nav_history.csv` | ~540K | Daily NAVs for 40 schemes (Jan 2022 - May 2026) |
| 3 | `03_aum_by_fund_house.csv` | ~200 | Quarterly AUM for top 10 AMCs |
| 4 | `04_monthly_sip_inflows.csv` | ~48 | Monthly macro SIP volume and industry AUM |
| 5 | `05_category_inflows.csv` | ~120 | Net inflows by fund category |
| 6 | `06_industry_folio_count.csv` | ~48 | Monthly investor folio growth |
| 7 | `07_scheme_performance.csv` | 40 | Trailing returns, Alpha, Beta, Sharpe, Drawdowns |
| 8 | `08_investor_transactions.csv` | 32K+ | SIP/Lumpsum/Redemption with demographics |
| 9 | `09_portfolio_holdings.csv` | ~800 | Sector allocations and stock weights |
| 10 | `10_benchmark_indices.csv` | ~2200 | Nifty 50, Nifty 100, Nifty Midcap 150 daily closes |

---

## Project Structure

```
.
├── run_pipeline.py                 # Master orchestration script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data_dictionary.md              # Database schema documentation
│
├── scripts/                        # All Python ETL & utility scripts
│   ├── README.md                   # Scripts documentation
│   ├── etl_pipeline.py             # Step 1: Data ingestion
│   ├── clean_data.py               # Step 2: Data cleaning & normalization
│   ├── db_load.py                  # Step 3: SQLite Star Schema loader
│   ├── compute_metrics.py          # Step 4: Performance metric computation
│   ├── recommender.py              # CLI fund recommendation engine
│   ├── live_nav_fetch.py           # Live NAV fetcher (mfapi.in)
│   ├── schedule_cron.sh            # Bonus B1: Cron job setup
│   ├── email_report.py             # Bonus B5: Automated HTML email
│   ├── generate_report.py          # Final Report PDF generator
│   └── generate_presentation.py    # Presentation PPTX generator
│
├── notebooks/                      # Jupyter analysis notebooks
│   ├── README.md                   # Notebooks documentation
│   ├── 01_data_ingestion.ipynb     # Data ingestion walkthrough
│   ├── 02_data_cleaning.ipynb      # Data cleaning walkthrough
│   ├── 03_eda_analysis.ipynb       # 10+ Plotly/Seaborn EDA charts
│   ├── 04_performance_analytics.ipynb  # Risk models & Fund Scorecards
│   └── 05_advanced_analytics.ipynb # VaR, Cohort, HHI, Monte Carlo, Markowitz
│
├── dashboard/                      # Streamlit web application
│   ├── README.md                   # Dashboard documentation
│   └── app.py                      # 4-page interactive dashboard
│
├── data/                           # Data directory (not committed to Git)
│   ├── README.md                   # Data documentation
│   ├── raw/                        # Original CSV files
│   ├── processed/                  # Cleaned CSVs
│   └── db/                         # SQLite database (bluestock_mf.db)
│
├── reports/                        # Generated outputs
│   ├── Final_Report.pdf            # Comprehensive capstone report (15+ pages)
│   ├── Bluestock_MF_Presentation.pptx  # 12-slide presentation deck
│   ├── charts/                     # PNG exports of all visualizations
│   └── data/                       # CSV exports (scorecard, VaR, etc.)
│
└── sql/                            # SQL assets
    ├── schema.sql                  # DDL for Star Schema creation
    └── queries.sql                 # 10 complex analytical queries
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kaushik-verse/-mutual-fund-analysis.git
   cd -mutual-fund-analysis
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   # venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## How to Run

### Option A: Full Pipeline (Recommended)
```bash
python run_pipeline.py
```
This executes: Ingestion -> Cleaning -> DB Load -> Metrics -> PDF & PPTX generation.

### Option B: Individual Steps
```bash
# ETL only (Steps 1-3)
python run_pipeline.py --etl

# Analytics only (Step 4)
python run_pipeline.py --analytics

# Reports only (Step 5)
python run_pipeline.py --report
```

### Option C: Manual Step-by-Step
```bash
python scripts/etl_pipeline.py        # Step 1: Ingest raw CSVs
python scripts/clean_data.py          # Step 2: Clean & normalize
python scripts/db_load.py             # Step 3: Load into SQLite
python scripts/compute_metrics.py     # Step 4: Generate metrics notebook
python scripts/generate_report.py     # Step 5a: Generate PDF report
python scripts/generate_presentation.py  # Step 5b: Generate PPTX
```

### Launch the Dashboard
```bash
streamlit run dashboard/app.py
```

### Run the Fund Recommender
```bash
python scripts/recommender.py          # Interactive prompt
python scripts/recommender.py High     # CLI argument
```

### SQL Analytics
```bash
sqlite3 data/db/bluestock_mf.db < sql/queries.sql
```

---

## Key Metrics Computed

| Metric | Formula | Purpose |
|--------|---------|---------|
| **CAGR** | `(NAV_end / NAV_start) ^ (252/N) - 1` | Annualized compounded returns |
| **Sharpe Ratio** | `(Rp - Rf) / Std(Rp) x sqrt(252)` | Risk-adjusted return (Rf = 6.5%) |
| **Sortino Ratio** | `(Rp - Rf) / Downside_Std x sqrt(252)` | Downside-only risk adjustment |
| **Alpha** | OLS intercept x 252 | Excess return over benchmark |
| **Beta** | OLS slope vs NIFTY 100 | Market volatility correlation |
| **Max Drawdown** | `min(NAV / Running_Max - 1)` | Worst peak-to-trough decline |
| **VaR (95%)** | 5th percentile of daily returns | Maximum expected daily loss |
| **CVaR** | Mean of returns below VaR | Expected loss in worst 5% of days |
| **HHI** | Sum of squared sector weights | Portfolio concentration index |

---

## Technologies Used

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.13 |
| **Data Processing** | Pandas, NumPy, SciPy |
| **Database** | SQLite3, SQLAlchemy |
| **Visualization** | Plotly, Seaborn, Matplotlib |
| **Dashboard** | Streamlit |
| **Reports** | fpdf2, python-pptx |
| **Automation** | Cron (bash), smtplib |
| **Notebooks** | Jupyter Lab, jupytext |
| **Version Control** | Git & GitHub |

---

## Bonus Challenges Completed (+50 marks)

| # | Challenge | Implementation |
|---|-----------|---------------|
| B1 | Cron Job Automation | `scripts/schedule_cron.sh` — weekday 8 PM NAV fetch |
| B2 | Streamlit Web App | `dashboard/app.py` — 4-page interactive dashboard |
| B3 | Monte Carlo Simulation | `05_advanced_analytics.ipynb` — 5-year NAV projections |
| B4 | Markowitz Optimization | `05_advanced_analytics.ipynb` — Efficient Frontier |
| B5 | Email Report Generator | `scripts/email_report.py` — automated HTML summaries |

---

*Disclaimer: NAVs and AUMs are based on publicly available AMFI data for educational purposes. Transactions are simulated for analytical demonstration. Mutual fund investments are subject to market risks.*
