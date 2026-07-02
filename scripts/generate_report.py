from fpdf import FPDF
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"

class PDF(FPDF):
    def header(self):
        # Draw a beautiful top margin bar
        self.set_fill_color(12, 35, 64) # Bluestock Navy
        self.rect(0, 0, 210, 15, 'F')
        
        self.set_y(18)
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(12, 35, 64)
        self.cell(0, 10, 'Bluestock Mutual Fund Analytics Capstone', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Comprehensive End-to-End Data Engineering & Analytics Pipeline', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        
        # Line separator
        self.set_draw_color(200, 200, 200)
        self.line(15, 36, 195, 36)
        self.ln(15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        
        # Line separator
        self.set_draw_color(200, 200, 200)
        self.line(15, 282, 195, 282)
        
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Author: Kaushik', align='C')
        
    def chapter_title(self, num, title):
        self.ln(5)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.set_fill_color(12, 35, 64) # Navy Blue
        self.cell(0, 10, f'  {num}. {title}', align='L', fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        
    def chapter_body(self, body):
        self.set_font('helvetica', '', 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, body)
        self.ln(5)

def generate_pdf():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Author & Date
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(12, 35, 64)
    pdf.cell(0, 8, 'Author: Kaushik', new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 5, 'Project: Bluestock Analytics', new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.ln(10)
    
    # 1. Executive Summary
    t1 = ("This report documents the architectural design, engineering implementation, and advanced analytical "
          "findings of the Bluestock Mutual Fund Analytics Capstone Project.\n\n"
          "The core objective was to aggregate highly fragmented mutual fund data representing over INR 81 Lakh Crore "
          "of Assets Under Management (AUM) into a centralized, analytical Star Schema. By achieving this, "
          "the platform provides institutional-grade risk metrics, interactive dashboarding, and automated "
          "reporting capabilities designed to drive data-driven investment decisions.")
    pdf.chapter_title(1, 'Executive Summary')
    pdf.chapter_body(t1)
    
    # 2. Data Engineering & ETL Pipeline
    t2 = ("The data engineering pipeline was fully automated using Python, Pandas, and SQLite, ensuring robust data integrity:\n\n"
          "- Data Ingestion: Automated extraction of 10 disparate CSV files encompassing historical NAVs, AUM figures, "
          "benchmarks, investor demographics, and transactions.\n"
          "- Data Cleansing: Missing dates in NAV histories were programmatically forward-filled to handle non-trading days. "
          "Deduplication and outlier removal were strictly enforced.\n"
          "- Dimensional Modeling: Data was meticulously mapped into a highly optimized 5-table Star Schema (fact_nav, "
          "fact_transactions, fact_performance, dim_fund, dim_date) to allow complex aggregations without performance bottlenecks.")
    pdf.chapter_title(2, 'Data Engineering & ETL Pipeline')
    pdf.chapter_body(t2)
    
    # 3. Quantitative Financial Modeling
    t3 = ("Extensive quantitative analysis was conducted to rank and evaluate the 40 mutual fund schemes:\n\n"
          "- Performance Metrics: Calculated 1-year, 3-year, and 5-year Compounded Annual Growth Rates (CAGR) utilizing exact "
          "252-day trading year formulas.\n"
          "- Risk-Adjusted Returns: Computed annualized Sharpe and Sortino ratios against a 6.5% risk-free rate proxy to isolate "
          "true management outperformance.\n"
          "- Benchmark Regressions: Executed Ordinary Least Squares (OLS) regressions against the NIFTY 100 benchmark to extract "
          "portfolio Alpha (excess returns) and Beta (market volatility correlation).\n"
          "- Downside Protection: Analyzed historical Maximum Drawdowns (peak-to-trough drops) to evaluate fund resilience during "
          "macroeconomic shocks.\n"
          "- Comprehensive Scorecard: Developed a proprietary 0-100 composite ranking system weighting trailing returns (30%), "
          "Sharpe ratios (25%), Alpha (20%), Expense Ratios (15%), and Drawdowns (10%).")
    pdf.chapter_title(3, 'Quantitative Financial Modeling')
    pdf.chapter_body(t3)
    
    pdf.add_page() # Start new page for advanced analytics
    
    # 4. Advanced Analytics & Machine Learning
    t4 = ("To provide deeper insights beyond standard historical trailing returns, advanced analytics and stochastic "
          "models were implemented:\n\n"
          "- Tail Risk Analysis (VaR): Calculated historical 95% Value-at-Risk (VaR) and Conditional VaR to quantify "
          "expected shortfall during extreme market downturns, exposing heavy tail-risks primarily in sectoral funds.\n"
          "- Sector Concentration: Computed the Herfindahl-Hirschman Index (HHI) for fund portfolios to mathematically "
          "highlight concentration risk.\n"
          "- Cohort Modeling: Grouped investors by their initial transaction year to monitor Systematic Investment Plan (SIP) "
          "stickiness, average step-up behaviors, and long-term brand loyalty.\n"
          "- Early Churn Detection: Flagged 'At-Risk' investors who exhibited SIP payment gaps exceeding 35 days, providing "
          "actionable intelligence for customer retention teams.")
    pdf.chapter_title(4, 'Advanced Analytics & Cohort Modeling')
    pdf.chapter_body(t4)
    
    # 5. Bonus Implementations
    t5 = ("Going above and beyond the baseline requirements, the following five bonus challenges were executed:\n\n"
          "1. Cron Automation (B1): Scheduled automated pipeline scripts to fetch and append daily NAV metrics.\n"
          "2. Interactive Web Application (B2): Deployed a real-time, 4-page Streamlit dashboard featuring interactive "
          "Plotly visualizations, dual-axis charts, and cross-filtering slicers.\n"
          "3. Stochastic Projections (B3): Engineered a Monte Carlo simulation running 100 iterations of 5-year future "
          "NAV trajectories, generating 5th, 50th, and 95th percentile expected bounds.\n"
          "4. Modern Portfolio Theory (B4): Programmed a Markowitz Efficient Frontier optimizer utilizing covariance "
          "matrices to discover the mathematical maximum Sharpe ratio portfolio allocation.\n"
          "5. Automated Email Reporting (B5): Built a script to construct and send dynamic HTML email reports summarizing "
          "weekly performance directly to management.")
    pdf.chapter_title(5, 'Bonus Challenges Accomplished')
    pdf.chapter_body(t5)
    
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    pdf.output(REPORT_DIR / 'Final_Report.pdf')
    print("Generated visually enhanced reports/Final_Report.pdf")

if __name__ == "__main__":
    generate_pdf()
