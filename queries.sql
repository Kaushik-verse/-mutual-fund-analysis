-- 1. Top 5 funds by latest AUM
SELECT f.scheme_name, a.aum_cr
FROM fact_aum a
JOIN dim_fund f ON a.scheme_code = f.scheme_code
WHERE a.as_of_date = (SELECT MAX(as_of_date) FROM fact_aum)
ORDER BY a.aum_cr DESC
LIMIT 5;

-- 2. Average NAV per month across all funds in 2026
SELECT d.year, d.month, f.scheme_name, AVG(n.nav) as avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
JOIN dim_fund f ON n.scheme_code = f.scheme_code
GROUP BY d.year, d.month, f.scheme_name
ORDER BY f.scheme_name, d.year, d.month;

-- 3. SIP Year-over-Year (YoY) Growth
WITH sip_yearly AS (
    SELECT d.year, SUM(t.amount) as total_sip
    FROM fact_transactions t
    JOIN dim_date d ON t.date = d.date
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
)
SELECT year, total_sip,
       LAG(total_sip) OVER(ORDER BY year) as prev_year_sip,
       ((total_sip - LAG(total_sip) OVER(ORDER BY year)) / LAG(total_sip) OVER(ORDER BY year)) * 100 as yoy_growth_percent
FROM sip_yearly;

-- 4. Transactions by State (Total volume and count)
SELECT state, COUNT(transaction_id) as txn_count, SUM(amount) as total_volume
FROM fact_transactions
GROUP BY state
ORDER BY total_volume DESC;

-- 5. Funds with expense_ratio < 1%
SELECT f.scheme_name, p.expense_ratio, p.as_of_date
FROM fact_performance p
JOIN dim_fund f ON p.scheme_code = f.scheme_code
WHERE p.expense_ratio < 1.0
ORDER BY p.expense_ratio ASC;

-- 6. Highest performing funds over 5 years
SELECT f.scheme_name, p.return_5y
FROM fact_performance p
JOIN dim_fund f ON p.scheme_code = f.scheme_code
WHERE p.is_anomaly = 0 AND p.return_5y IS NOT NULL
ORDER BY p.return_5y DESC
LIMIT 5;

-- 7. Redemption vs Lumpsum Volume Ratio per month
SELECT d.year, d.month, 
       SUM(CASE WHEN t.transaction_type = 'REDEMPTION' THEN t.amount ELSE 0 END) as total_redemptions,
       SUM(CASE WHEN t.transaction_type = 'LUMPSUM' THEN t.amount ELSE 0 END) as total_lumpsum
FROM fact_transactions t
JOIN dim_date d ON t.date = d.date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 8. KYC Status Breakdown of Transactions
SELECT kyc_status, COUNT(transaction_id) as count, SUM(amount) as total_amount
FROM fact_transactions
GROUP BY kyc_status;

-- 9. Volatility check: Max and Min NAV per scheme in the last 30 days
SELECT f.scheme_name, MAX(n.nav) as max_nav, MIN(n.nav) as min_nav, 
       (MAX(n.nav) - MIN(n.nav)) / MIN(n.nav) * 100 as volatility_percent
FROM fact_nav n
JOIN dim_fund f ON n.scheme_code = f.scheme_code
WHERE n.date >= date((SELECT MAX(date) FROM fact_nav), '-30 days')
GROUP BY f.scheme_name
ORDER BY volatility_percent DESC;

-- 10. Fund House AUM Market Share
WITH latest_aum AS (
    SELECT scheme_code, aum_cr
    FROM fact_aum
    WHERE as_of_date = (SELECT MAX(as_of_date) FROM fact_aum)
)
SELECT f.fund_house, SUM(a.aum_cr) as total_aum
FROM latest_aum a
JOIN dim_fund f ON a.scheme_code = f.scheme_code
GROUP BY f.fund_house
ORDER BY total_aum DESC;
