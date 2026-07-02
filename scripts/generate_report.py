from fpdf import FPDF
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(12, 35, 64) # Bluestock Navy
        self.cell(0, 10, 'Bluestock Mutual Fund Analytics Capstone Report', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def generate_pdf():
    pdf = PDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('helvetica', 'B', 24)
    pdf.cell(0, 20, 'Final Capstone Report', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, 'Author: Bluestock Data Engineering Team', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    
    # Executive Summary
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Executive Summary', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    text1 = ("This report outlines the end-to-end data engineering and analytics pipeline built for the "
             "Indian Mutual Fund industry. Over INR 81 Lakh Crore of AUM data, 32,000+ investor transactions, "
             "and 40 top-performing schemes were ingested, cleaned, and modeled into a robust SQLite Star Schema.")
    pdf.multi_cell(0, 8, text1)
    pdf.ln(5)
    
    # Methodology
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '2. ETL & Data Modeling Methodology', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    text2 = ("- Data Ingestion: Automated fetch of historical NAV, AUM, and portfolio CSVs.\n"
             "- Data Cleaning: Addressed missing values using forward-fill, normalized transaction dates, "
             "and standardized fund naming conventions.\n"
             "- Star Schema: Built around fact_nav, fact_transactions, and fact_performance, connected to "
             "dim_fund and dim_date.")
    pdf.multi_cell(0, 8, text2)
    pdf.ln(5)
    
    # Key Insights
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '3. Advanced Analytical Insights', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    text3 = ("1. Risk-Adjusted Dominance: Top tier funds maintained a Sharpe > 1.2 despite macro volatility.\n"
             "2. Sectoral Tail Risk: Value-at-Risk (VaR) calculations exposed heavy tail risks in sectoral funds, "
             "corroborated by high HHI concentration.\n"
             "3. SIP Stickiness: Cohort analysis proved that early adopters maintain active SIPs with a churn "
             "risk flagged at >35 days of inactivity.")
    pdf.multi_cell(0, 8, text3)
    pdf.ln(5)
    
    # Bonus Implementation
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '4. Bonus Challenges Implemented', new_x="LMARGIN", new_y="NEXT")
    pdf.set_font('helvetica', '', 11)
    text4 = ("- Cron job automation for live NAV fetching.\n"
             "- Monte Carlo simulations for 5-year NAV projections.\n"
             "- Markowitz Efficient Frontier optimization.\n"
             "- Interactive Streamlit Web Dashboard deployment.\n"
             "- Automated HTML Email Report generation.")
    pdf.multi_cell(0, 8, text4)
    
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    pdf.output(REPORT_DIR / 'Final_Report.pdf')
    print("Generated reports/Final_Report.pdf")

if __name__ == "__main__":
    generate_pdf()
