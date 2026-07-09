#!/usr/bin/env python3
"""
run_pipeline.py — Master orchestration script for the Bluestock MF Capstone.

Executes the full ETL-to-Analytics pipeline in the correct sequence:
  1. Data Ingestion   (scripts/etl_pipeline.py)
  2. Data Cleaning     (scripts/clean_data.py)
  3. Database Loading  (scripts/db_load.py)
  4. Metric Computation (scripts/compute_metrics.py)
  5. Report Generation  (scripts/generate_report.py + generate_presentation.py)

Usage:
    python run_pipeline.py          # Run everything
    python run_pipeline.py --etl    # Run only ETL steps (1-3)
    python run_pipeline.py --report # Run only report generation (5)

Author: Kaushik
"""

import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR / "scripts"
PYTHON = sys.executable


def run_step(name, script):
    """Execute a pipeline step and exit on failure."""
    print(f"\n{'='*60}")
    print(f"  STEP: {name}")
    print(f"{'='*60}")
    result = subprocess.run([PYTHON, str(script)], cwd=str(BASE_DIR))
    if result.returncode != 0:
        print(f"\n[ERROR] Step '{name}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"  [OK] {name} completed successfully.")


def run_etl():
    """Run ETL pipeline steps 1-3."""
    run_step("1. Data Ingestion", SCRIPTS_DIR / "etl_pipeline.py")
    run_step("2. Data Cleaning", SCRIPTS_DIR / "clean_data.py")
    run_step("3. Database Loading", SCRIPTS_DIR / "db_load.py")


def run_analytics():
    """Run metric computation (step 4)."""
    run_step("4. Performance Metric Computation", SCRIPTS_DIR / "compute_metrics.py")


def run_reports():
    """Run report and presentation generation (step 5)."""
    run_step("5a. Final Report (PDF)", SCRIPTS_DIR / "generate_report.py")
    run_step("5b. Presentation (PPTX)", SCRIPTS_DIR / "generate_presentation.py")


def main():
    """Main pipeline orchestrator."""
    print("=" * 60)
    print("  BLUESTOCK MUTUAL FUND ANALYTICS PIPELINE")
    print("  Author: Kaushik")
    print("=" * 60)

    args = set(sys.argv[1:])

    if "--etl" in args:
        run_etl()
    elif "--report" in args:
        run_reports()
    elif "--analytics" in args:
        run_analytics()
    else:
        # Full pipeline
        run_etl()
        run_analytics()
        run_reports()

    print(f"\n{'='*60}")
    print("  PIPELINE COMPLETE")
    print(f"{'='*60}")
    print("  Outputs:")
    print(f"    Database:     data/db/bluestock_mf.db")
    print(f"    PDF Report:   reports/Final_Report.pdf")
    print(f"    Presentation: reports/Bluestock_MF_Presentation.pptx")
    print(f"    Dashboard:    streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()
