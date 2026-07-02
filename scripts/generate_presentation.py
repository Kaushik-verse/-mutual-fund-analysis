from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
REPORT_DIR = BASE_DIR / "reports"

def generate_presentation():
    prs = Presentation()
    
    # Slide 1: Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Bluestock Mutual Fund Analytics"
    subtitle.text = "Capstone Project Presentation\nEnd-to-End Data Engineering & Analytics"
    
    # Slide 2: Project Architecture
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "Project Architecture & ETL Pipeline"
    tf = body_shape.text_frame
    tf.text = "Ingestion of 10 raw CSV datasets covering NAVs, AUM, and transactions."
    
    p = tf.add_paragraph()
    p.text = "Automated Data Cleaning using Pandas (ffill, deduplication)."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Normalized into a 5-Table SQLite Star Schema."
    p.level = 1
    
    # Slide 3: Advanced Analytics
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "Advanced Quantitative Modeling"
    tf = body_shape.text_frame
    tf.text = "Calculated Alpha, Beta, Sharpe, and Sortino ratios."
    
    p = tf.add_paragraph()
    p.text = "Historical Value at Risk (VaR) and Conditional VaR computed."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "Bonus: Markowitz Portfolio Optimization & Monte Carlo Simulations."
    p.level = 1
    
    # Slide 4: Conclusion
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    
    title_shape.text = "Deliverables & Conclusion"
    tf = body_shape.text_frame
    tf.text = "Fully interactive Streamlit Dashboard developed."
    
    p = tf.add_paragraph()
    p.text = "Automated email reporting systems configured."
    p.level = 1
    
    p = tf.add_paragraph()
    p.text = "All project rubrics and bonus challenges successfully met."
    p.level = 1
    
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    prs.save(REPORT_DIR / 'Presentation.pptx')
    print("Generated reports/Presentation.pptx")

if __name__ == "__main__":
    generate_presentation()
