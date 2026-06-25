# Bluestock Mutual Fund Data Dictionary

This document outlines the data structure for the SQLite Star Schema (`bluestock_mf.db`) generated for the Mutual Fund Analysis project.

## Database Overview
- **Database**: SQLite (`bluestock_mf.db`)
- **Design**: Star Schema
- **Fact Tables**: `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`, `fact_dividend`
- **Dimension Tables**: `dim_fund`, `dim_date`, `dim_investor`, `dim_distributor`, `dim_market_index`, `dim_fund_manager`

---

## Dimension Tables

### `dim_fund`
Master table of mutual fund schemes.
- `scheme_code` (INTEGER): **PRIMARY KEY**. Unique AMFI identifier for the scheme.
- `scheme_name` (TEXT): Full name of the mutual fund scheme.
- `fund_house` (TEXT): The Asset Management Company (AMC) managing the fund.
- `scheme_type` (TEXT): Type of scheme (e.g., Open Ended).
- `scheme_category` (TEXT): Category of the fund (e.g., Equity Scheme - Large Cap Fund).
- `isin_growth` (TEXT): ISIN number for the Growth plan.
- `isin_div_reinvestment` (TEXT): ISIN number for Dividend Reinvestment plan.

### `dim_date`
Master calendar dimension table.
- `date` (TEXT): **PRIMARY KEY**. Format YYYY-MM-DD.
- `year` (INTEGER): 4-digit year.
- `month` (INTEGER): Month number (1-12).
- `day` (INTEGER): Day of the month.
- `quarter` (INTEGER): Quarter of the year (1-4).
- `day_of_week` (INTEGER): Day of the week (0=Monday, 6=Sunday).
- `is_weekend` (BOOLEAN): True if Saturday/Sunday.

### `dim_investor`
Metadata about investors.
- `investor_id` (TEXT): **PRIMARY KEY**. Unique identifier for the investor.
- `age` (INTEGER): Age of the investor.

### `dim_distributor`
Platform or distributor entities.
- `dist_id` (TEXT): **PRIMARY KEY**. Unique identifier for the distributor.
- `name` (TEXT): Name of the distributor (e.g., Zerodha, Groww).

### `dim_market_index`
Market indices mapped for benchmarks.
- `index_code` (TEXT): **PRIMARY KEY**. Short code for index (e.g., NIFTY50).
- `name` (TEXT): Full name of the index.

### `dim_fund_manager`
Managers running the funds.
- `manager_id` (INTEGER): **PRIMARY KEY**. Auto-increment ID.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `manager` (TEXT): Name of the fund manager.

---

## Fact Tables

### `fact_nav`
Daily Net Asset Value history.
- `nav_id` (INTEGER): **PRIMARY KEY**. Auto-increment ID.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `date` (TEXT): **FOREIGN KEY**. References `dim_date(date)`.
- `nav` (REAL): Net Asset Value on the given date. Missing holidays/weekends are forward-filled.

### `fact_transactions`
Records of investor inflows/outflows.
- `transaction_id` (TEXT): **PRIMARY KEY**. Unique transaction identifier.
- `investor_id` (TEXT): **FOREIGN KEY**. References `dim_investor(investor_id)`.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `date` (TEXT): **FOREIGN KEY**. References `dim_date(date)`.
- `transaction_type` (TEXT): Standardized type (`SIP`, `LUMPSUM`, `REDEMPTION`).
- `amount` (REAL): Transaction volume in currency.
- `state` (TEXT): Origin state of the transaction.
- `kyc_status` (TEXT): Enum of investor KYC state (`VERIFIED`, `PENDING`, `REJECTED`).

### `fact_performance`
Periodic performance metrics and expense ratios.
- `performance_id` (INTEGER): **PRIMARY KEY**. Auto-increment ID.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `as_of_date` (TEXT): **FOREIGN KEY**. References `dim_date(date)`.
- `return_1y` (REAL): 1-year trailing percentage return.
- `return_3y` (REAL): 3-year trailing percentage return.
- `return_5y` (REAL): 5-year trailing percentage return.
- `expense_ratio` (REAL): Total Expense Ratio (TER) in percentage (valid range 0.1% - 2.5%).
- `is_anomaly` (BOOLEAN): True if any return metric exceeded 100%.

### `fact_aum`
Assets Under Management records.
- `aum_id` (INTEGER): **PRIMARY KEY**. Auto-increment ID.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `as_of_date` (TEXT): **FOREIGN KEY**. References `dim_date(date)`.
- `aum_cr` (REAL): Asset Under Management in Crores.

### `fact_dividend`
Historical dividend distributions.
- `dividend_id` (INTEGER): **PRIMARY KEY**. Auto-increment ID.
- `scheme_code` (INTEGER): **FOREIGN KEY**. References `dim_fund(scheme_code)`.
- `dividend` (REAL): Dividend amount distributed.
