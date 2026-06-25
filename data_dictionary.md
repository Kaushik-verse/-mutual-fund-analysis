# Data Dictionary: Bluestock MF Capstone

This document defines the variables and tables populated in `bluestock_mf.db`.

## 1. dim_fund
Dimension table storing fund metadata.
- **amfi_code** (INTEGER): Primary Key. AMFI unique scheme code.
- **fund_house** (TEXT): AMC name.
- **scheme_name** (TEXT): Full scheme name.
- **category** (TEXT): Equity / Debt / Hybrid.
- **sub_category** (TEXT): Large Cap, Mid Cap, etc.
- **plan** (TEXT): Regular or Direct.
- **launch_date** (DATE): Scheme launch date.
- **benchmark** (TEXT): Official benchmark index.
- **expense_ratio_pct** (REAL): Annual expense ratio.
- **exit_load_pct** (REAL): Exit load percentage.
- **min_sip_amount** (INTEGER): Minimum SIP amount allowed.
- **min_lumpsum_amount** (INTEGER): Minimum Lumpsum amount allowed.
- **fund_manager** (TEXT): Name of primary manager.
- **risk_category** (TEXT): SEBI risk category.
- **sebi_category_code** (TEXT): Internal category code.

## 2. fact_nav
Fact table containing daily NAV history.
- **amfi_code** (INTEGER): Foreign Key to dim_fund.
- **date** (DATE): NAV Date.
- **nav** (REAL): Net Asset Value in INR.

## 3. fact_transactions
Fact table containing individual investor transactions.
- **investor_id** (TEXT): Unique investor ID.
- **transaction_date** (DATE): Date of transaction.
- **amfi_code** (INTEGER): Foreign Key to dim_fund.
- **transaction_type** (TEXT): Sip, Lumpsum, or Redemption.
- **amount_inr** (INTEGER): Transaction amount.
- **state** (TEXT): Investor state.
- **city** (TEXT): Investor city.
- **city_tier** (TEXT): T30 or B30 classification.
- **age_group** (TEXT): Age bracket.
- **gender** (TEXT): Male/Female.
- **annual_income_lakh** (REAL): Annual income.
- **payment_mode** (TEXT): UPI, Cheque, Net Banking, etc.
- **kyc_status** (TEXT): Verified/Pending.

## 4. fact_performance
Fact table summarizing historical performance and risk metrics.
- **amfi_code** (INTEGER): Foreign Key to dim_fund.
- **scheme_name** (TEXT): Scheme Name.
- **fund_house** (TEXT): AMC.
- **category** (TEXT): Scheme Category.
- **plan** (TEXT): Scheme Plan.
- **return_1yr_pct** (REAL): 1-year trailing return.
- **return_3yr_pct** (REAL): 3-year trailing return.
- **return_5yr_pct** (REAL): 5-year trailing return.
- **benchmark_3yr_pct** (REAL): 3-year benchmark return.
- **alpha** (REAL): Alpha vs Benchmark.
- **beta** (REAL): Beta vs Benchmark.
- **sharpe_ratio** (REAL): Risk-adjusted return metric.
- **sortino_ratio** (REAL): Downside risk-adjusted metric.
- **std_dev_ann_pct** (REAL): Annualized volatility.
- **max_drawdown_pct** (REAL): Maximum drawdown.
- **aum_crore** (INTEGER): Current AUM in Crores.
- **expense_ratio_pct** (REAL): Expense Ratio.
- **morningstar_rating** (INTEGER): Star rating.
- **risk_grade** (TEXT): Risk Grade.

## 5. fact_aum
Fact table tracking quarterly AUM totals per fund house.
- **date** (DATE): Snapshot date.
- **fund_house** (TEXT): AMC name.
- **aum_lakh_crore** (REAL): AUM in Lakh Crores.
- **aum_crore** (INTEGER): AUM in Crores.
- **num_schemes** (INTEGER): Total active schemes.

## 6. fact_sip_industry
Fact table tracking macro SIP inflows into the MF industry.
- **month** (TEXT): YYYY-MM.
- **sip_inflow_crore** (INTEGER): Total SIP inflow.
- **active_sip_accounts_crore** (REAL): Number of active accounts.
- **new_sip_accounts_lakh** (REAL): New account registrations.
- **sip_aum_lakh_crore** (REAL): Total SIP AUM.
- **yoy_growth_pct** (REAL): YoY growth.

## 7. fact_portfolio
Fact table tracking equity portfolio allocations per scheme.
- **amfi_code** (INTEGER): Foreign Key to dim_fund.
- **stock_symbol** (TEXT): Ticker symbol.
- **stock_name** (TEXT): Company Name.
- **sector** (TEXT): Industry Sector.
- **weight_pct** (REAL): Portfolio Weight %.
- **market_value_cr** (REAL): Absolute Market Value (Cr).
- **current_price_inr** (REAL): Stock Price.
- **portfolio_date** (DATE): Snapshot Date.

## 8. dim_date / fact_benchmark
Dimension table for dates and benchmark performance tracking.
- **date** (DATE): Date key.
- **index_name** (TEXT): e.g. NIFTY50.
- **close_value** (REAL): Daily closing level.
