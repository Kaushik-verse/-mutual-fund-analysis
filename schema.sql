-- Dimension Tables

CREATE TABLE dim_fund (
    scheme_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    scheme_type TEXT,
    scheme_category TEXT,
    isin_growth TEXT,
    isin_div_reinvestment TEXT
);

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    is_weekend BOOLEAN
);

-- Fact Tables

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    date TEXT,
    nav REAL,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE fact_transactions (
    transaction_id TEXT PRIMARY KEY,
    investor_id TEXT,
    scheme_code INTEGER,
    date TEXT,
    transaction_type TEXT,
    amount REAL,
    state TEXT,
    kyc_status TEXT,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY(date) REFERENCES dim_date(date)
);

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    as_of_date TEXT,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    expense_ratio REAL,
    is_anomaly BOOLEAN,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY(as_of_date) REFERENCES dim_date(date)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    as_of_date TEXT,
    aum_cr REAL,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code),
    FOREIGN KEY(as_of_date) REFERENCES dim_date(date)
);

-- Other tables from our 10 datasets
CREATE TABLE dim_investor (
    investor_id TEXT PRIMARY KEY,
    age INTEGER
);

CREATE TABLE dim_distributor (
    dist_id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE dim_market_index (
    index_code TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE dim_fund_manager (
    manager_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    manager TEXT,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code)
);

CREATE TABLE fact_dividend (
    dividend_id INTEGER PRIMARY KEY AUTOINCREMENT,
    scheme_code INTEGER,
    dividend REAL,
    FOREIGN KEY(scheme_code) REFERENCES dim_fund(scheme_code)
);
