# Dashboard Directory

This directory contains the Streamlit interactive web application for the Bluestock MF Analytics platform.

## Overview

`app.py` is a 4-page interactive dashboard built with **Streamlit** and **Plotly** as an alternative to Power BI (which lacks native macOS support). It connects directly to the SQLite Star Schema (`data/db/bluestock_mf.db`).

## Pages

| Page | Content |
|------|---------|
| **Industry Overview** | KPI cards (AUM, SIP, Folios, Schemes), AUM trend line, AUM by AMC bar chart |
| **Fund Performance** | Return vs Risk scatter plot (bubble = AUM), sortable scorecard table, NAV vs benchmark line |
| **Investor Analytics** | Transaction amount by state, SIP/Lumpsum/Redemption split donut, age group SIP analysis, monthly volume |
| **SIP & Market Trends** | Dual-axis SIP inflow + Nifty 50 chart, category flow heatmap, top 5 categories by inflow |

## How to Run

```bash
# From project root
streamlit run dashboard/app.py
```

The dashboard will open at `http://localhost:8501`.
