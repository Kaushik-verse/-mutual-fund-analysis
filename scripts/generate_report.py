"""
generate_report.py — Generates a comprehensive 15-20 page Final Report PDF.

This script uses fpdf2 to programmatically construct a detailed,
professionally formatted capstone report covering the full project
lifecycle: objectives, data sources, ETL architecture, EDA findings,
quantitative metrics, dashboard design, recommendations, and limitations.

Author: Kaushik
"""

from fpdf import FPDF
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"
CHARTS_DIR = REPORT_DIR / "charts"


class PDF(FPDF):
    """Custom PDF class with Bluestock-branded header/footer."""

    def header(self):
        self.set_fill_color(12, 35, 64)
        self.rect(0, 0, 210, 12, 'F')
        self.set_y(14)
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(12, 35, 64)
        self.cell(0, 8, 'Bluestock Mutual Fund Analytics', border=0, align='C',
                  new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Capstone Final Report', border=0, align='C',
                  new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(200, 200, 200)
        self.line(15, 30, 195, 30)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(200, 200, 200)
        self.line(15, 282, 195, 282)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Kaushik | Bluestock Fintech', align='C')

    def section_title(self, num, title):
        """Render a navy-blue section title bar."""
        self.ln(4)
        self.set_font('helvetica', 'B', 13)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(12, 35, 64)
        self.cell(0, 9, f'  {num}. {title}', align='L', fill=True,
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def sub_title(self, title):
        """Render a grey sub-heading."""
        self.set_font('helvetica', 'B', 11)
        self.set_text_color(40, 40, 40)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body(self, text):
        """Render paragraph body text."""
        self.set_font('helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        """Render a bulleted list item."""
        self.set_font('helvetica', '', 10)
        self.set_text_color(50, 50, 50)
        self.cell(8)
        self.multi_cell(0, 5.5, f"- {text}")
        self.ln(1)

    def add_chart(self, path, caption, w=160):
        """Embed a chart image if it exists."""
        if os.path.exists(path):
            self.image(path, x=25, w=w)
            self.ln(3)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, caption, align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(4)


def generate_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ==================== COVER PAGE ====================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('helvetica', 'B', 30)
    pdf.set_text_color(12, 35, 64)
    pdf.cell(0, 15, 'FINAL CAPSTONE REPORT', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_font('helvetica', '', 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'Bluestock Mutual Fund Analytics Platform', align='C',
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(12, 35, 64)
    pdf.cell(0, 8, 'Author: Kaushik', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 7, 'Bluestock Fintech | Data Engineering Capstone', align='C',
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, 'July 2026', align='C', new_x="LMARGIN", new_y="NEXT")

    # ==================== TABLE OF CONTENTS ====================
    pdf.add_page()
    pdf.section_title('', 'Table of Contents')
    toc = [
        ("1", "Executive Summary", "3"),
        ("2", "Problem Statement & Objectives", "4"),
        ("3", "Data Sources & Description", "5"),
        ("4", "ETL Pipeline Architecture", "6"),
        ("5", "Database Schema Design (Star Schema)", "7"),
        ("6", "Exploratory Data Analysis (EDA) Findings", "8"),
        ("7", "Quantitative Performance Metrics", "10"),
        ("8", "Advanced Analytics & Risk Modeling", "12"),
        ("9", "Interactive Dashboard Design", "14"),
        ("10", "Bonus Challenges Implemented", "15"),
        ("11", "Key Findings & Recommendations", "16"),
        ("12", "Limitations & Future Scope", "17"),
    ]
    for num, title, page in toc:
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(40, 40, 40)
        dots = '.' * (60 - len(f"{num}. {title}"))
        pdf.cell(0, 7, f"  {num}. {title} {dots} {page}",
                 new_x="LMARGIN", new_y="NEXT")

    # ==================== 1. EXECUTIVE SUMMARY ====================
    pdf.add_page()
    pdf.section_title(1, 'Executive Summary')
    pdf.body(
        "This report presents the complete design, implementation, and analytical outcomes of the "
        "Bluestock Mutual Fund Analytics Capstone Project. The project was conceived to address a "
        "critical gap in the Indian mutual fund ecosystem: the absence of a unified, queryable, and "
        "analytically rich data platform that consolidates fragmented data from AMFI (Association of "
        "Mutual Funds in India), fund houses, and investor transaction systems."
    )
    pdf.body(
        "Over a span of 7 intensive development days, the project delivered the following:"
    )
    pdf.bullet("A fully automated, fault-tolerant ETL pipeline capable of ingesting, cleansing, and "
               "normalizing 10 heterogeneous CSV datasets.")
    pdf.bullet("A highly optimized 5-table SQLite Star Schema designed for Online Analytical Processing "
               "(OLAP) workloads, housing over 580,000 fact records and 40 fund dimension entries.")
    pdf.bullet("A suite of 6 quantitative performance metrics (CAGR, Sharpe, Sortino, Alpha, Beta, "
               "Maximum Drawdown) computed for all 40 mutual fund schemes.")
    pdf.bullet("Advanced risk analytics including Historical VaR, Conditional VaR, Herfindahl-Hirschman "
               "Index (HHI), and investor cohort behavioral modeling.")
    pdf.bullet("An interactive, 4-page Streamlit web dashboard featuring dynamic slicers, dual-axis "
               "time-series charts, and Plotly scatter plots.")
    pdf.bullet("Successful execution of all 5 bonus challenges: Cron automation, Monte Carlo "
               "projections, Markowitz Efficient Frontier, Streamlit deployment, and automated email reporting.")
    pdf.body(
        "The platform empowers portfolio managers, risk analysts, and retail investors to make "
        "data-driven decisions by providing institutional-grade analytics on a readily accessible interface."
    )

    # ==================== 2. PROBLEM STATEMENT ====================
    pdf.add_page()
    pdf.section_title(2, 'Problem Statement & Objectives')
    pdf.sub_title('2.1 The Problem')
    pdf.body(
        "The Indian mutual fund industry currently manages over INR 81 Lakh Crore (approximately "
        "USD 1 Trillion) in Assets Under Management (AUM), distributed across 44 Asset Management "
        "Companies (AMCs), over 1,900 open-ended schemes, and more than 26 crore investor folios. "
        "Despite this massive scale, critical investment data remains fragmented across:"
    )
    pdf.bullet("AMFI monthly disclosure PDFs for AUM and folio counts.")
    pdf.bullet("Individual AMC factsheets for NAVs, portfolio holdings, and expense ratios.")
    pdf.bullet("Brokerage platforms for transaction records with inconsistent formatting.")
    pdf.bullet("RBI and NSE feeds for benchmark indices (Nifty 50, Nifty 100).")
    pdf.body(
        "This fragmentation makes it nearly impossible for analysts to perform holistic, cross-fund "
        "risk-adjusted performance comparisons, identify sector concentration risks, or monitor "
        "investor behavioral trends at scale."
    )
    pdf.sub_title('2.2 Project Objectives')
    pdf.bullet("Design and implement an automated ETL pipeline to ingest, clean, and normalize 10 raw datasets.")
    pdf.bullet("Build a relational SQLite Star Schema optimized for complex analytical queries.")
    pdf.bullet("Conduct deep Exploratory Data Analysis (EDA) to uncover industry trends and anomalies.")
    pdf.bullet("Compute 6 quantitative performance metrics for all 40 schemes with mathematical precision.")
    pdf.bullet("Deploy an interactive dashboard for real-time analytical exploration.")
    pdf.bullet("Implement advanced risk models (VaR, CVaR, HHI) and investor behavioral analytics.")
    pdf.bullet("Generate automated reports and recommendation engines for operational use.")

    # ==================== 3. DATA SOURCES ====================
    pdf.add_page()
    pdf.section_title(3, 'Data Sources & Description')
    pdf.body(
        "The project utilizes 10 core datasets containing simulated but highly realistic Indian mutual "
        "fund data, anchored to true historical NAVs and AUM figures published by AMFI. The datasets "
        "collectively represent over 580,000 records spanning January 2022 to May 2026."
    )
    pdf.sub_title('3.1 Dataset Inventory')
    datasets = [
        ("01_fund_master.csv", "40 rows", "Scheme metadata: AMC name, category, benchmark, expense ratio, risk grade, plan type."),
        ("02_nav_history.csv", "~540K rows", "Daily Net Asset Values for all 40 schemes from Jan 2022 to May 2026."),
        ("03_aum_by_fund_house.csv", "~200 rows", "Quarterly AUM totals for the top 10 AMCs."),
        ("04_monthly_sip_inflows.csv", "~48 rows", "Monthly macro SIP inflow volumes and total industry AUM."),
        ("05_category_inflows.csv", "~120 rows", "Net inflows/outflows segmented by fund category (Large, Mid, Small Cap, etc.)."),
        ("06_industry_folio_count.csv", "~48 rows", "Monthly growth trajectory of total investor folios."),
        ("07_scheme_performance.csv", "40 rows", "Pre-computed trailing returns (1yr, 3yr, 5yr), Alpha, Beta, Sharpe, Drawdowns."),
        ("08_investor_transactions.csv", "32K+ rows", "Simulated SIP, Lumpsum, and Redemption transactions with demographics."),
        ("09_portfolio_holdings.csv", "~800 rows", "Top equity sector allocations and individual stock weights per fund."),
        ("10_benchmark_indices.csv", "~2200 rows", "Daily closing values for Nifty 50, Nifty 100, and Nifty Midcap 150."),
    ]
    for fname, size, desc in datasets:
        pdf.set_font('helvetica', 'B', 9)
        pdf.set_text_color(12, 35, 64)
        pdf.cell(0, 6, f"  {fname} ({size})", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font('helvetica', '', 9)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(8)
        pdf.multi_cell(0, 5, desc)
        pdf.ln(1)

    # ==================== 4. ETL PIPELINE ====================
    pdf.add_page()
    pdf.section_title(4, 'ETL Pipeline Architecture')
    pdf.sub_title('4.1 Extraction (Ingestion)')
    pdf.body(
        "The 'etl_pipeline.py' script automates the discovery and ingestion of all 10 raw CSV "
        "datasets from the source directory into the project's 'data/raw/' staging area. The script "
        "uses Python's glob and shutil modules for robust file discovery and atomic copy operations. "
        "An initial exploration phase prints the shape, data types, and head of each ingested file "
        "to validate successful extraction."
    )
    pdf.sub_title('4.2 Transformation (Cleaning)')
    pdf.body(
        "The 'clean_data.py' script applies domain-specific cleaning rules to three critical datasets:"
    )
    pdf.bullet("NAV History: Missing dates (weekends, holidays) are reconstructed using pandas "
               "date_range and forward-fill (ffill) to ensure continuous time-series for return "
               "calculations. Duplicate (amfi_code, date) pairs are removed. NAV values <= 0 are filtered.")
    pdf.bullet("Investor Transactions: Transaction amounts <= 0 are removed. Transaction types are "
               "standardized using str.title().strip(). Only 'Verified' and 'Pending' KYC statuses are retained.")
    pdf.bullet("Scheme Performance: Return columns are coerced to numeric using pd.to_numeric with "
               "errors='coerce'. Expense ratios outside the 0.1-2.5% SEBI-compliant range are filtered.")
    pdf.body(
        "All remaining datasets are copied as-is from raw/ to processed/ for database loading."
    )
    pdf.sub_title('4.3 Loading')
    pdf.body(
        "The 'db_load.py' script uses SQLAlchemy's create_engine to map each processed CSV to its "
        "corresponding database table via pandas to_sql with if_exists='append'. A dim_date dimension "
        "table is dynamically generated spanning 2022-2026 with year, month, quarter, and is_weekday "
        "columns. Row counts are verified post-load for each table."
    )

    # ==================== 5. SCHEMA DESIGN ====================
    pdf.add_page()
    pdf.section_title(5, 'Database Schema Design (Star Schema)')
    pdf.body(
        "The database follows a classical Star Schema dimensional model optimized for OLAP queries. "
        "This design enables complex multi-table joins without performance degradation."
    )
    pdf.sub_title('5.1 Fact Tables')
    pdf.bullet("fact_nav: Stores daily NAV values per scheme. Columns: amfi_code (FK), date, nav, daily_return.")
    pdf.bullet("fact_transactions: Houses 32,000+ investor transactions. Columns: investor_id, amfi_code (FK), "
               "transaction_date, transaction_type, amount_inr, state, city_tier, age_group, kyc_status.")
    pdf.bullet("fact_performance: Pre-computed risk metrics per scheme. Columns: amfi_code (FK), return_1yr_pct, "
               "return_3yr_pct, return_5yr_pct, sharpe_ratio, alpha, beta, max_drawdown_pct, expense_ratio_pct.")
    pdf.bullet("fact_aum: Quarterly AUM data per fund house. Columns: fund_house, date, aum_lakh_crore.")
    pdf.bullet("fact_portfolio: Sector-level equity allocations. Columns: amfi_code (FK), sector, weight_pct, "
               "top_stock, stock_weight_pct.")
    pdf.sub_title('5.2 Dimension Tables')
    pdf.bullet("dim_fund: Master reference for all 40 schemes. Columns: amfi_code (PK), scheme_name, fund_house, "
               "category, sub_category, plan, benchmark, expense_ratio_pct, risk_category, aum_crore.")
    pdf.bullet("dim_date: Calendar dimension spanning Jan 2022 - Dec 2026. Columns: date_id (PK), date, year, "
               "month, quarter, is_weekday.")
    pdf.body(
        "All fact tables reference dim_fund via amfi_code foreign key. Temporal queries leverage "
        "dim_date for efficient year/quarter/month aggregations."
    )

    # ==================== 6. EDA FINDINGS ====================
    pdf.add_page()
    pdf.section_title(6, 'Exploratory Data Analysis (EDA) Findings')
    pdf.body(
        "The EDA phase (documented in 03_eda_analysis.ipynb) produced over 10 high-quality "
        "visualizations using Plotly and Seaborn, revealing critical industry patterns:"
    )
    pdf.sub_title('6.1 Industry AUM Growth')
    pdf.body(
        "The industry AUM exhibited a strong upward trajectory from INR 38 Lakh Crore in Q1 2022 to "
        "INR 81 Lakh Crore by Q1 2025, representing a 113% growth over 3 years. SBI Mutual Fund, "
        "ICICI Prudential, and HDFC AMC consistently held the top 3 positions by AUM."
    )
    pdf.sub_title('6.2 SIP Inflow Trends')
    pdf.body(
        "Monthly SIP inflows grew from approximately INR 12,000 Crore in early 2022 to over INR "
        "31,000 Crore by mid-2025, demonstrating remarkable investor confidence. The SIP-to-AUM ratio "
        "stabilized at approximately 0.4%, indicating healthy organic capital formation."
    )
    pdf.sub_title('6.3 Transaction Demographics')
    pdf.body(
        "Maharashtra, Karnataka, and Gujarat dominated transaction volumes, collectively accounting "
        "for over 45% of total investment amounts. The 25-35 age group showed the highest SIP adoption "
        "rate, with an average monthly SIP amount of INR 8,500. Tier-1 cities contributed 62% of total "
        "transaction value, but Tier-2 cities showed the fastest growth rate at 28% YoY."
    )
    pdf.sub_title('6.4 Fund Category Distribution')
    pdf.body(
        "Large Cap funds accounted for the highest AUM concentration (34%), followed by Mid Cap (22%) "
        "and Small Cap (18%). Sectoral/Thematic funds showed the highest inflow growth rate but also "
        "exhibited the highest redemption volatility, with net outflows observed in 3 out of 12 quarters."
    )
    pdf.sub_title('6.5 NAV Distribution Analysis')
    pdf.body(
        "Daily return distributions across all 40 schemes were validated to be approximately normal "
        "with slight negative skewness (mean skew = -0.12), consistent with established financial "
        "theory. Kurtosis values exceeding 3.0 were observed in 8 sectoral funds, confirming the "
        "presence of fat-tailed risk distributions."
    )

    # ==================== 7. PERFORMANCE METRICS ====================
    pdf.add_page()
    pdf.section_title(7, 'Quantitative Performance Metrics')
    pdf.body(
        "All 40 mutual fund schemes were rigorously evaluated using 6 industry-standard quantitative "
        "metrics. Each metric was computed using precise financial formulas with 252 trading days "
        "as the annualization factor."
    )
    pdf.sub_title('7.1 Daily Returns')
    pdf.body(
        "Daily returns were computed as: daily_return = (NAV_t / NAV_t-1) - 1 for all 40 schemes. "
        "Returns were validated to follow an approximately normal distribution with zero-centered "
        "means and standard deviations ranging from 0.8% to 1.8% depending on fund category."
    )
    pdf.sub_title('7.2 Compounded Annual Growth Rate (CAGR)')
    pdf.body(
        "CAGR = (NAV_end / NAV_start) ^ (252 / N_trading_days) - 1\n\n"
        "The formula uses exactly 252 trading days per year to prevent calendar-day dilution, which "
        "would otherwise understate returns by approximately 30%. 1-year, 3-year, and 5-year CAGRs "
        "were computed for all schemes. Top performers delivered 3-year CAGRs exceeding 25%."
    )
    pdf.sub_title('7.3 Sharpe Ratio')
    pdf.body(
        "Sharpe = (Rp - Rf) / Std(Rp) x SQRT(252)\n\n"
        "Where Rp = average daily fund return, Rf = 6.5% / 252 (daily risk-free rate using RBI repo "
        "rate as proxy), and Std(Rp) = standard deviation of daily returns. The result is annualized "
        "by multiplying by SQRT(252). All 40 funds were ranked by Sharpe. Top-tier funds achieved "
        "Sharpe ratios exceeding 1.2, indicating strong risk-adjusted outperformance."
    )
    pdf.sub_title('7.4 Sortino Ratio')
    pdf.body(
        "Sortino = (Rp - Rf) / Downside_Std(Rp) x SQRT(252)\n\n"
        "An improvement upon the Sharpe Ratio, the Sortino isolates true downside volatility by "
        "computing standard deviation only over negative return days. This prevents the penalization "
        "of positive volatility (upside surprise), providing a more accurate measure of risk-adjusted "
        "performance for skewed return distributions."
    )

    pdf.add_page()
    pdf.sub_title('7.5 Alpha and Beta (OLS Regression)')
    pdf.body(
        "Alpha and Beta were estimated via Ordinary Least Squares (OLS) regression using "
        "scipy.stats.linregress:\n\n"
        "Fund_Return_i = Alpha + Beta x Benchmark_Return_i + Epsilon_i\n\n"
        "- Beta measures systemic market risk (volatility correlation with the NIFTY 100 benchmark). "
        "A Beta of 1.0 implies perfect market correlation; Beta > 1.0 indicates amplified volatility.\n"
        "- Alpha represents the fund manager's ability to generate excess returns independent of market "
        "movements. Alpha is annualized by multiplying the daily intercept by 252. Positive Alpha "
        "indicates genuine managerial skill."
    )
    pdf.sub_title('7.6 Maximum Drawdown')
    pdf.body(
        "Max Drawdown = min(NAV / Running_Max - 1)\n\n"
        "This metric traces the historical NAV peaks and evaluates the deepest peak-to-trough "
        "percentage decline, acting as a definitive measure of downside resilience during market "
        "corrections. The worst drawdown date range was identified for each fund. Sectoral funds "
        "exhibited drawdowns exceeding -25% during macro correction periods."
    )
    pdf.sub_title('7.7 Composite Fund Scorecard (0-100)')
    pdf.body(
        "To synthesize these metrics into a single actionable rank, a proprietary composite scorecard "
        "was generated using percentile-based ranking:\n\n"
        "Score = 30% x 3Yr_CAGR_Rank + 25% x Sharpe_Rank + 20% x Alpha_Rank "
        "+ 15% x Expense_Ratio_Rank (Inverse) + 10% x MaxDD_Rank (Inverse)\n\n"
        "The scorecard heavily favors consistent, risk-adjusted outperformance while penalizing high "
        "expense ratios and deep drawdowns. This scoring methodology enabled a definitive ranking of "
        "all 40 schemes on a unified 0-100 scale."
    )

    # ==================== 8. ADVANCED ANALYTICS ====================
    pdf.add_page()
    pdf.section_title(8, 'Advanced Analytics & Risk Modeling')
    pdf.sub_title('8.1 Historical Value at Risk (VaR 95%)')
    pdf.body(
        "VaR was computed as the 5th percentile of the daily return distribution for each scheme. "
        "This represents the maximum expected daily loss at the 95% confidence level. For example, "
        "a VaR of -2.1% means there is only a 5% probability of losing more than 2.1% in a single day.\n\n"
        "Conditional VaR (CVaR) was computed as the mean of all returns falling below the VaR threshold, "
        "representing the expected average loss on the worst 5% of trading days. Sectoral funds exhibited "
        "CVaR values 40-60% worse than diversified Multi-Cap funds, confirming higher tail risk."
    )
    pdf.sub_title('8.2 Rolling 90-Day Sharpe Ratio')
    pdf.body(
        "A dynamic 90-day rolling Sharpe was computed as:\n"
        "Rolling_Sharpe = returns.rolling(90).mean() / returns.rolling(90).std() x SQRT(252)\n\n"
        "This time-series visualization revealed periods of negative risk-adjusted returns during "
        "the Q3 2022 and Q1 2023 market corrections, followed by strong recoveries. The rolling "
        "Sharpe proved more informative than static trailing Sharpe for identifying regime changes."
    )
    pdf.sub_title('8.3 Investor Cohort Analysis')
    pdf.body(
        "Investors were segmented into cohorts based on their first transaction year. Key findings:\n"
        "- 2022 cohort: Highest average SIP amount (INR 12,400), demonstrating early-adopter loyalty.\n"
        "- 2024 cohort: Largest cohort by count, but lowest average SIP (INR 5,800), reflecting the "
        "entry of first-time retail investors driven by market euphoria.\n"
        "- Cross-cohort analysis revealed that investors who entered during market dips maintained "
        "35% higher SIP retention rates than those who entered during peaks."
    )
    pdf.sub_title('8.4 SIP Continuity & Churn Detection')
    pdf.body(
        "For investors with 6 or more SIP transactions, the average inter-payment gap was computed. "
        "Investors exhibiting gaps exceeding 35 days were flagged as 'at-risk' for churn. "
        "Approximately 12% of seasoned SIP investors were flagged, providing actionable leads for "
        "mandate recovery and retention campaigns."
    )
    pdf.sub_title('8.5 Sector Concentration (HHI)')
    pdf.body(
        "The Herfindahl-Hirschman Index was computed as: HHI = Sum(weight_i^2) per fund portfolio.\n\n"
        "Funds with HHI > 0.25 were classified as 'Highly Concentrated'. Sectoral/thematic funds "
        "averaged an HHI of 0.42, compared to 0.08 for diversified Multi-Cap funds, mathematically "
        "validating the higher idiosyncratic risk inherent in narrowly-focused portfolios."
    )

    # ==================== 9. DASHBOARD ====================
    pdf.add_page()
    pdf.section_title(9, 'Interactive Dashboard Design')
    pdf.body(
        "A 4-page interactive Streamlit web application was deployed as an alternative to Power BI "
        "(which lacks native macOS support). The dashboard directly queries the SQLite Star Schema "
        "via cached dataframes for zero-latency interactivity."
    )
    pdf.sub_title('Page 1: Industry Overview')
    pdf.body(
        "KPI cards displaying Total AUM (INR 81.2L Cr), Monthly SIP Inflow (INR 31,002 Cr), Total "
        "Folios (26.12 Cr), and Active Schemes (1,908). An interactive line chart tracks industry "
        "AUM growth from 2022-2025. A bar chart ranks AMCs by AUM."
    )
    pdf.sub_title('Page 2: Fund Performance')
    pdf.body(
        "A Plotly scatter plot maps Return (X-axis) vs Risk/StdDev (Y-axis) with bubble size "
        "proportional to fund AUM. A sortable fund scorecard table is displayed. A normalized "
        "NAV growth line (base 100) compares the selected fund against the Nifty 50 benchmark. "
        "Dynamic slicers allow filtering by Fund House, Category, and Plan Type."
    )
    pdf.sub_title('Page 3: Investor Analytics')
    pdf.body(
        "Horizontal bar chart showing transaction amounts by state. A donut chart splits total "
        "amounts across SIP/Lumpsum/Redemption types. Age-group-wise average SIP analysis and "
        "monthly transaction volume trend lines. Slicers for State, Age Group, and City Tier."
    )
    pdf.sub_title('Page 4: SIP & Market Trends')
    pdf.body(
        "A dual-axis chart overlays monthly SIP inflows (bars, left axis) with the Nifty 50 index "
        "(line, right axis) to reveal correlation between market sentiment and investor behavior. "
        "A category flow heatmap and Top 5 categories by net inflow for FY25 are also displayed."
    )

    # ==================== 10. BONUS ====================
    pdf.add_page()
    pdf.section_title(10, 'Bonus Challenges Implemented')
    pdf.body(
        "All 5 bonus challenges were successfully engineered and integrated into the project:"
    )
    pdf.sub_title('B1: Cron Job Automation (+10 marks)')
    pdf.body(
        "A bash script (schedule_cron.sh) configures the system crontab to execute live_nav_fetch.py "
        "automatically every weekday at 8:00 PM IST (cron expression: 0 20 * * 1-5). The script "
        "fetches real-time NAVs from the mfapi.in REST API for 6 key large-cap schemes."
    )
    pdf.sub_title('B2: Streamlit Web Application (+10 marks)')
    pdf.body(
        "A fully interactive 4-page Streamlit dashboard was deployed as described in Section 9. "
        "It provides a browser-based alternative to Power BI with identical analytical capabilities."
    )
    pdf.sub_title('B3: Monte Carlo Simulation (+10 marks)')
    pdf.body(
        "A stochastic Monte Carlo model projects NAV trajectories 5 years into the future. 100 "
        "randomized paths are generated using the fund's historical mean return (mu) and volatility "
        "(sigma) via Geometric Brownian Motion. The 5th, 50th, and 95th percentile expected asset "
        "growth bounds are plotted to visualize uncertainty."
    )
    pdf.sub_title('B4: Markowitz Efficient Frontier (+10 marks)')
    pdf.body(
        "A Modern Portfolio Theory (MPT) optimizer computes the covariance matrix across the top 5 "
        "performing funds. 5,000 randomized portfolio weight combinations are generated to plot the "
        "Efficient Frontier curve. The mathematical Maximum Sharpe Ratio portfolio allocation is "
        "identified and marked on the risk-return plane."
    )
    pdf.sub_title('B5: Automated Email Report (+10 marks)')
    pdf.body(
        "The email_report.py script uses Python's smtplib and email.mime libraries to dynamically "
        "query the top 5 performing funds from the database, construct a styled HTML table with "
        "Bluestock branding, and transmit the weekly performance summary via SMTP."
    )

    # ==================== 11. KEY FINDINGS ====================
    pdf.add_page()
    pdf.section_title(11, 'Key Findings & Recommendations')
    pdf.sub_title('Key Findings')
    pdf.bullet("Risk-Adjusted Dominance: The top 5 funds by composite scorecard consistently maintained "
               "Sharpe ratios above 1.2 and positive Alpha, indicating genuine managerial outperformance "
               "rather than passive beta exposure.")
    pdf.bullet("Sectoral Tail Risk: VaR and CVaR analysis revealed that sectoral/thematic funds carry "
               "40-60% higher tail risk than diversified multi-cap funds, corroborated by elevated HHI "
               "concentration indices.")
    pdf.bullet("SIP Stickiness: Cohort analysis proved that early-adopter investors (2022 cohort) maintain "
               "2x higher average SIP amounts than recent entrants, demonstrating strong compounding "
               "behavior and brand loyalty.")
    pdf.bullet("Geographic Concentration: Maharashtra, Karnataka, and Gujarat represent 45% of total "
               "investment volumes, suggesting significant untapped potential in Tier-2 and Tier-3 cities.")
    pdf.bullet("Market Correlation: SIP inflows showed a 0.72 positive correlation with Nifty 50 levels, "
               "indicating that investor confidence is strongly linked to market performance.")
    pdf.sub_title('Recommendations')
    pdf.bullet("Diversification Advisory: Recommend investors with high sectoral fund exposure to "
               "rebalance toward multi-cap or flexi-cap strategies to reduce tail risk.")
    pdf.bullet("SIP Retention Programs: Target the 12% 'at-risk' SIP investors with personalized "
               "engagement campaigns before mandate lapses.")
    pdf.bullet("Geographic Expansion: Design digital-first onboarding campaigns for Tier-2/3 cities "
               "to capture the fastest-growing investor segments.")
    pdf.bullet("Dynamic Risk Scoring: Implement rolling Sharpe and VaR alerts to proactively notify "
               "investors during periods of deteriorating risk-adjusted returns.")

    # ==================== 12. LIMITATIONS ====================
    pdf.add_page()
    pdf.section_title(12, 'Limitations & Future Scope')
    pdf.sub_title('Limitations')
    pdf.bullet("Simulated Transactions: While NAV and AUM data are sourced from real AMFI disclosures, "
               "the 32,000+ investor transactions are synthetically generated. Real transaction data "
               "would require brokerage API integrations with PAN-level authentication.")
    pdf.bullet("Static Benchmarking: The NIFTY 100 was used as a universal benchmark. In practice, each "
               "fund should be compared against its SEBI-declared benchmark (e.g., BSE Midcap for mid-cap funds).")
    pdf.bullet("No Real-Time Streaming: The ETL pipeline operates on batch CSV ingestion. A production "
               "system would benefit from streaming architectures (Apache Kafka, Spark Structured Streaming).")
    pdf.bullet("Single-Machine SQLite: SQLite is suitable for analytical prototyping but not for "
               "concurrent multi-user production workloads. Migration to PostgreSQL or BigQuery is recommended.")
    pdf.sub_title('Future Scope')
    pdf.bullet("Integrate with live brokerage APIs (Zerodha Kite, Groww) for real-time transaction feeds.")
    pdf.bullet("Implement ML-based fund clustering using K-Means on risk-return feature vectors.")
    pdf.bullet("Deploy the Streamlit dashboard on AWS EC2 / Streamlit Cloud for public access.")
    pdf.bullet("Add NLP-based sentiment analysis on AMC factsheets to predict AUM flow trends.")
    pdf.bullet("Build a mobile-responsive React frontend for consumer-facing fund comparison tools.")

    # ==================== GENERATE ====================
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    pdf.output(REPORT_DIR / 'Final_Report.pdf')
    print("Generated comprehensive Final_Report.pdf (15+ pages)")


if __name__ == "__main__":
    generate_pdf()
