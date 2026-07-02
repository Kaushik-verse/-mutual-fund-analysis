from fpdf import FPDF
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"

class PDF(FPDF):
    def header(self):
        self.set_fill_color(12, 35, 64) # Bluestock Navy
        self.rect(0, 0, 210, 15, 'F')
        
        self.set_y(18)
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(12, 35, 64)
        self.cell(0, 10, 'Bluestock Mutual Fund Analytics Capstone', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Comprehensive End-to-End Data Engineering & Analytics Pipeline', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        
        self.set_draw_color(200, 200, 200)
        self.line(15, 36, 195, 36)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(200, 200, 200)
        self.line(15, 282, 195, 282)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Author: Kaushik', align='C')
        
    def chapter_title(self, num, title):
        self.ln(5)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(12, 35, 64)
        self.cell(0, 10, f'  {num}. {title}', align='L', fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('helvetica', '', 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, body)
        self.ln(2)

def generate_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Author
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(12, 35, 64)
    pdf.cell(0, 8, 'Author: Kaushik', new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 5, 'Project: Bluestock Analytics', new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.ln(5)
    
    # 1. Introduction
    t1 = ("The Bluestock Mutual Fund Analytics Capstone Project is a comprehensive, enterprise-grade data engineering and quantitative analytics platform. "
          "The Indian mutual fund industry currently manages over INR 81 Lakh Crore (approximately $1 Trillion USD) in Assets Under Management (AUM), distributed across thousands of schemes, millions of investor folios, and diverse asset classes. "
          "Despite this massive scale, institutional and retail investors alike struggle with fragmented data, making it difficult to holistically evaluate risk-adjusted performance, macro-industry trends, and portfolio concentration risks.\n\n"
          "This project bridges that gap by engineering an end-to-end Extract, Transform, and Load (ETL) pipeline that ingests simulated historical NAVs, AUM figures, macroeconomic benchmarks (NIFTY 50/100), and a corpus of over 32,000 investor transactions. "
          "The ultimate output is a highly structured, query-optimized SQLite Star Schema database that powers rigorous quantitative modeling, interactive visualizations, and an automated recommendation engine. "
          "The platform enables deep, data-driven investment analysis, allowing analysts to rapidly evaluate mutual fund outperformance, isolate downside tail risks, and monitor client behavioral stickiness.")
    pdf.chapter_title(1, 'Project Introduction & Objectives')
    pdf.chapter_body(t1)
    
    # 2. Data Engineering Architecture
    t2 = ("The architectural backbone of this platform relies on an automated, fault-tolerant Python ETL pipeline designed to transform chaotic raw CSV datasets into a relational database model optimized for Online Analytical Processing (OLAP).\n\n"
          "- Data Ingestion: The 'etl_pipeline.py' script automates the discovery and ingestion of 10 disparate raw datasets representing fund metadata, historical NAVs, portfolio holdings, AUM trajectories, and investor transaction logs.\n\n"
          "- Data Cleansing & Normalization: Financial time-series data is notoriously sparse due to market holidays and weekends. To ensure continuous return calculations, missing dates within the NAV histories were imputed using programmatic forward-fill (ffill) algorithms. "
          "Transaction datasets underwent strict validation filters to remove negative transaction amounts, standardize categorical variables (e.g., standardizing 'sip' to 'Sip'), and isolate pending or verified KYC statuses.\n\n"
          "- Star Schema Dimensional Modeling: The cleansed datasets were loaded into a central SQLite database ('bluestock_mf.db') utilizing SQLAlchemy. The database is strictly organized into a 5-table Star Schema. "
          "The central fact tables ('fact_nav', 'fact_transactions', 'fact_performance', 'fact_aum', 'fact_portfolio') house granular, time-series metrics. These are explicitly linked via primary and foreign keys to dimension tables "
          "('dim_fund' for scheme metadata, 'dim_date' for temporal grouping), enabling instantaneous, complex multi-table SQL joins and rapid metric aggregations.")
    pdf.chapter_title(2, 'Data Engineering & ETL Architecture')
    pdf.chapter_body(t2)
    
    # 3. Quantitative Performance Metrics
    t3 = ("To objectively evaluate the 40 mutual fund schemes, we implemented a suite of advanced quantitative financial models written in Python (Pandas/NumPy/SciPy):\n\n"
          "- Compounded Annual Growth Rate (CAGR): Evaluates the annualized return over 1, 3, and 5-year periods. Crucially, to prevent calendar-day dilution, the formula was calibrated to utilize exactly 252 trading days per year: "
          "CAGR = (Ending Value / Beginning Value) ^ (252 / N_Trading_Days) - 1.\n\n"
          "- Sharpe Ratio: Quantifies risk-adjusted returns by subtracting the risk-free rate (proxy set at the 6.5% RBI repo rate) from the fund's average daily return, divided by the standard deviation of returns. The result is multiplied by SQRT(252) to annualize the metric.\n\n"
          "- Sortino Ratio: An improvement upon the Sharpe Ratio, the Sortino Ratio isolates true downside volatility. The denominator strictly measures the standard deviation of negative return days, preventing the penalization of upside volatility.\n\n"
          "- Alpha and Beta (OLS Regression): Computed via Ordinary Least Squares regression against the NIFTY 100 benchmark. 'Beta' measures the fund's systemic market risk (volatility correlation), while 'Alpha' (annualized by 252) isolates the manager's ability to generate excess returns independent of macro market movements.\n\n"
          "- Maximum Drawdown: Mathematically traces the historical NAV peaks and evaluates the deepest peak-to-trough percentage drop, acting as a definitive measure of historical downside resilience during market crashes.\n\n"
          "- Bluestock Composite Scorecard: To synthesize these metrics into a single, actionable rank, a 0-100 percentile scorecard was generated. The weighting algorithm heavily favors consistent, risk-adjusted outperformance: "
          "3-Year CAGR (30%), Sharpe Ratio (25%), Alpha (20%), Expense Ratio (15% Inverse), and Maximum Drawdown (10% Inverse).")
    pdf.chapter_title(3, 'Quantitative Financial Metrics')
    pdf.chapter_body(t3)
    
    pdf.add_page()
    
    # 4. Advanced Analytics & Cohort Modeling
    t4 = ("The analytical pipeline extended beyond standard performance metrics into advanced behavioral and risk modeling:\n\n"
          "- Tail Risk Analysis (VaR & CVaR): Standard deviation assumes a normal distribution, which often fails during black-swan market crashes. We computed the historical 95% Value-at-Risk (VaR), pinpointing the 5th percentile worst daily return. "
          "Furthermore, Conditional VaR (CVaR) was calculated to measure the expected average loss strictly on days when the VaR threshold is breached. These metrics exposed that Sectoral funds harbor significantly higher tail-risks than Multi-Cap funds.\n\n"
          "- Sector Concentration (HHI): The Herfindahl-Hirschman Index (HHI) was calculated by summing the squared percentage weights of individual sector allocations within each portfolio. Funds approaching an HHI of 1.0 are highly concentrated, mathematically validating their increased idiosyncratic risk.\n\n"
          "- Investor Cohort Analysis: Investors were segmented into cohorts based on their initial onboarding year. By tracking these cohorts chronologically, the platform revealed that earlier cohorts exhibit significantly higher average Systematic Investment Plan (SIP) amounts, demonstrating the power of compounding brand trust and step-up SIP behaviors.\n\n"
          "- Early Churn Detection (At-Risk SIPs): The transaction logs of seasoned investors (6+ active SIPs) were parsed to calculate the average gap in days between successful payments. Investors exhibiting average payment intervals exceeding 35 days were programmatically flagged as 'At-Risk', providing the business with immediate leads for churn-prevention and mandate recovery.")
    pdf.chapter_title(4, 'Advanced Analytics & Cohort Modeling')
    pdf.chapter_body(t4)
    
    # 5. Bonus Implementations
    t5 = ("To maximize the operational value of the platform, five advanced bonus capabilities were successfully engineered and integrated:\n\n"
          "1. Cron Automation (B1): We deployed a bash automation script ('schedule_cron.sh') configuring the system crontab to execute the live NAV fetching pipeline automatically every Monday through Friday at exactly 8:00 PM, ensuring the database remains perfectly synchronized with live market closes.\n\n"
          "2. Interactive Streamlit Dashboard (B2): Moving beyond static BI tools, a bespoke Python web application was deployed using Streamlit. The dashboard directly queries the SQLite Star Schema via cached dataframes to deliver a zero-latency, 4-page interactive interface featuring dynamic slicers, dual-axis charts, and Plotly scatter plots comparing Fund Risk vs Return.\n\n"
          "3. Monte Carlo Simulations (B3): A stochastic Monte Carlo model was engineered to project NAV trajectories 5 years into the future. By iterating 100 randomized paths utilizing the fund's historical mean return (mu) and volatility (sigma), the model visually plots the 5th, 50th, and 95th percentile expected asset growth bounds.\n\n"
          "4. Markowitz Efficient Frontier (B4): Grounded in Modern Portfolio Theory (MPT), an optimizer was programmed to calculate the covariance matrix across the top 5 performing funds. By generating 5,000 randomized portfolio weightings, the model plots the 'Efficient Frontier' and isolates the exact allocation required to achieve the mathematical Maximum Sharpe Ratio.\n\n"
          "5. Automated Email Reporting (B5): Built an automation script ('email_report.py') utilizing the Python 'smtplib' and 'email.mime' libraries. The script dynamically queries the top 5 funds from the database, constructs a styled HTML table, and transmits the weekly performance summary directly to executive management via an SMTP server.")
    pdf.chapter_title(5, 'Bonus Capstone Implementations')
    pdf.chapter_body(t5)
    
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    pdf.output(REPORT_DIR / 'Final_Report.pdf')
    print("Generated ultra-detailed Final_Report.pdf")

if __name__ == "__main__":
    generate_pdf()
