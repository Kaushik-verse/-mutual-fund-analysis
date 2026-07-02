from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"

def set_text(shape, text, bold=False, size=16, color=RGBColor(0, 0, 0)):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.bold = bold
    run.font.size = Pt(size)
    run.font.color.rgb = color

def generate_presentation():
    prs = Presentation()
    
    # -------------------------------------------------------------
    # Slide 1: Title Slide
    # -------------------------------------------------------------
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Bluestock Mutual Fund Analytics Platform"
    title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    title.text_frame.paragraphs[0].font.bold = True
    
    subtitle.text = "Capstone Project Presentation\nEnd-to-End Data Engineering & Advanced Quantitative Analytics\nAuthor: Kaushik"
    subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
    
    # -------------------------------------------------------------
    # Slide 2: Project Objectives & Scope
    # -------------------------------------------------------------
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "1. Project Objectives & Scope"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    
    tf = slide.placeholders[1].text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "The Challenge: Fragmented Data in a $1 Trillion Industry"
    p.font.bold = True
    p.font.size = Pt(20)
    
    p = tf.add_paragraph()
    p.text = "The Indian MF industry manages INR 81 Lakh Crore, yet data is siloed across AMFI reports, brokerages, and static PDFs, preventing real-time, holistic risk assessment."
    p.level = 1
    p.font.size = Pt(16)
    
    p = tf.add_paragraph()
    p.text = "The Solution: A Centralized Analytics Engine"
    p.font.bold = True
    p.font.size = Pt(20)
    
    p = tf.add_paragraph()
    p.text = "Engineered a Python-based ETL pipeline to ingest 10 massive datasets (historical NAVs, 32k+ investor transactions, benchmark indices)."
    p.level = 1
    p.font.size = Pt(16)
    
    p = tf.add_paragraph()
    p.text = "Modeled into a highly optimized SQLite Star Schema to power instant, zero-latency quantitative algorithms and interactive dashboards."
    p.level = 1
    p.font.size = Pt(16)

    # -------------------------------------------------------------
    # Slide 3: Data Engineering & ETL Architecture
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "2. Data Engineering & ETL Architecture"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    
    tf = slide.placeholders[1].text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "Robust Cleansing & Normalization Protocols"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Implemented programmatic forward-fill (ffill) logic to reconstruct missing NAV values during market weekends and holidays."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "The Star Schema Dimensional Model"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Fact Tables: fact_nav, fact_transactions, fact_performance, fact_aum, fact_portfolio. Captures raw, temporal, and quantifiable metrics."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Dimension Tables: dim_fund (scheme metadata, risk profiles), dim_date (temporal mapping). Enables rapid cross-table SQL joins."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Bonus B1: Automation"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Designed a bash chron-job to automatically execute the live NAV fetching pipeline every weekday at exactly 8:00 PM."
    p.level = 1

    # -------------------------------------------------------------
    # Slide 4: Quantitative Financial Modeling
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "3. Quantitative Financial Modeling"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    
    tf = slide.placeholders[1].text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "Precision Performance Metrics"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Calculated annualized Compounded Annual Growth Rates (CAGR) utilizing strict 252 trading-day logic to prevent calendar-day dilution."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Risk-Adjusted Outperformance & Benchmark Tracking"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Computed annualized Sharpe & Sortino Ratios using a 6.5% risk-free rate proxy to isolate managerial outperformance against volatility."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Executed Ordinary Least Squares (OLS) regression against NIFTY 100 to map systemic Beta risk and alpha-generation."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "The Composite Scorecard"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Synthesized metrics into a 0-100 percentile rank: 3Yr CAGR (30%), Sharpe (25%), Alpha (20%), Expense Ratio (15%), Maximum Drawdown (10%)."
    p.level = 1

    # -------------------------------------------------------------
    # Slide 5: Advanced Analytics & Behavioral Modeling
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "4. Advanced Analytics & Behavioral Modeling"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    
    tf = slide.placeholders[1].text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "Tail-Risk & Sector Concentration"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Calculated 95% Value-at-Risk (VaR) and Conditional VaR to quantify expected shortfalls during black-swan events."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Computed the Herfindahl-Hirschman Index (HHI) for portfolios, mathematically exposing the high concentration risk inherent in Sectoral funds."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Investor Cohort & Churn Analytics"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Grouped investors by their initial onboarding year to prove that early cohorts maintain significantly higher SIP capital allocations."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Programmatically flagged 'At-Risk' users who exhibited SIP payment gaps exceeding 35 days, providing actionable retention leads."
    p.level = 1

    # -------------------------------------------------------------
    # Slide 6: Bonus Deliverables & Final Architecture
    # -------------------------------------------------------------
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "5. Bonus Deliverables Achieved"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(12, 35, 64)
    
    tf = slide.placeholders[1].text_frame
    tf.clear()
    
    p = tf.paragraphs[0]
    p.text = "We executed 100% of the Capstone Bonus Challenges:"
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "[B1] Cron automation script deployed for live, hands-free NAV syncing."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "[B2] An interactive 4-page Streamlit Dashboard was deployed, featuring dual-axis charts, risk-return scatter plots, and dynamic filtering."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "[B3] Stochastic Monte Carlo Simulations engineered to project 5-year NAV growth paths, generating 5th, 50th, and 95th percentile expected asset bounds."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "[B4] Markowitz Efficient Frontier models deployed to compute covariance matrices and discover the mathematical Maximum Sharpe Ratio portfolio allocation."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "[B5] Automated SMTP email scripts engineered to dynamically construct and transmit HTML weekly performance summaries to executive management."
    p.level = 1

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(REPORT_DIR / 'Presentation.pptx')
    print("Generated ultra-detailed Presentation.pptx")

if __name__ == "__main__":
    generate_presentation()
