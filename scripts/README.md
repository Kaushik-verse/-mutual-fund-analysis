# Scripts Directory

This directory contains all Python ETL scripts, utility modules, and automation tools for the Bluestock Mutual Fund Analytics platform.

## Script Inventory

| Script | Purpose | Run Command |
|--------|---------|-------------|
| `etl_pipeline.py` | Ingests 10 raw CSV datasets into `data/raw/` | `python scripts/etl_pipeline.py` |
| `clean_data.py` | Cleans NAV history (ffill), transactions, and performance data | `python scripts/clean_data.py` |
| `db_load.py` | Loads processed CSVs into the SQLite Star Schema | `python scripts/db_load.py` |
| `compute_metrics.py` | Generates the Day 4 performance analytics notebook | `python scripts/compute_metrics.py` |
| `recommender.py` | CLI fund recommender by risk appetite (Low/Moderate/High) | `python scripts/recommender.py` |
| `live_nav_fetch.py` | Fetches real-time NAVs from mfapi.in REST API | `python scripts/live_nav_fetch.py` |
| `schedule_cron.sh` | Sets up a cron job for automated weekday NAV fetching | `bash scripts/schedule_cron.sh` |
| `email_report.py` | Generates and sends automated HTML email performance reports | `python scripts/email_report.py` |
| `generate_report.py` | Generates the 15+ page Final_Report.pdf using fpdf2 | `python scripts/generate_report.py` |
| `generate_presentation.py` | Generates 12-slide Bluestock_MF_Presentation.pptx | `python scripts/generate_presentation.py` |
