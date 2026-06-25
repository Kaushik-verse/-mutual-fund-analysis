-- 1. Top 5 funds by AUM
SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    aum_crore 
FROM fact_performance 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month for SBI Bluechip (119551)
SELECT 
    strftime('%Y-%m', date) as month, 
    AVG(nav) as avg_nav 
FROM fact_nav 
WHERE amfi_code = 119551 
GROUP BY month 
ORDER BY month;

-- 3. SIP inflow YoY growth
SELECT 
    month, 
    sip_inflow_crore, 
    yoy_growth_pct 
FROM fact_sip_industry 
ORDER BY month;

-- 4. Transactions by state (Volume and Amount)
SELECT 
    state, 
    COUNT(*) as total_transactions, 
    SUM(amount_inr) as total_amount_inr 
FROM fact_transactions 
GROUP BY state 
ORDER BY total_amount_inr DESC;

-- 5. Funds with expense_ratio < 1%
SELECT 
    amfi_code, 
    scheme_name, 
    expense_ratio_pct 
FROM dim_fund 
WHERE expense_ratio_pct < 1.0 
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 Equity Funds by 3-Year Return
SELECT 
    amfi_code, 
    scheme_name, 
    return_3yr_pct 
FROM fact_performance 
WHERE category = 'Equity' 
ORDER BY return_3yr_pct DESC 
LIMIT 5;

-- 7. Total SIP amount by Age Group
SELECT 
    age_group, 
    SUM(amount_inr) as total_sip_inr 
FROM fact_transactions 
WHERE transaction_type = 'Sip' 
GROUP BY age_group 
ORDER BY total_sip_inr DESC;

-- 8. Top 5 Holdings in HDFC Top 100
SELECT 
    stock_symbol, 
    stock_name, 
    weight_pct 
FROM fact_portfolio 
WHERE amfi_code = 125497 
ORDER BY weight_pct DESC 
LIMIT 5;

-- 9. AUM by Fund House (Latest)
SELECT 
    fund_house, 
    SUM(aum_crore) as total_aum_crore 
FROM fact_aum 
GROUP BY fund_house 
ORDER BY total_aum_crore DESC;

-- 10. Best Funds by Sharpe Ratio (Moderate Risk)
SELECT 
    amfi_code, 
    scheme_name, 
    sharpe_ratio 
FROM fact_performance 
WHERE risk_grade = 'Moderate' 
ORDER BY sharpe_ratio DESC 
LIMIT 5;
