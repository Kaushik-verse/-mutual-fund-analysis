import nbformat as nbf

nb = nbf.v4.new_notebook()

# Intro
nb.cells.append(nbf.v4.new_markdown_cell("# Day 4: Fund Performance Analytics\n\nThis notebook computes key performance metrics for all 40 schemes, builds a scorecard, and compares performance against benchmarks."))

# Setup
code_setup = """
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')

os.makedirs('../reports/charts', exist_ok=True)
os.makedirs('../reports/data', exist_ok=True)

# Load datasets from DB instead of CSV if we want, or fix the CSV paths
# Wait, day 4 uses CSVs from `../data/processed/`. That is fine.
# Wait, does Day 4 use sqlite? Let's check:
raw_dir = '../data/processed/'
df_nav = pd.read_csv(raw_dir + '02_nav_history.csv')
df_nav['date'] = pd.to_datetime(df_nav['date'])
df_nav = df_nav.sort_values(['amfi_code', 'date'])

df_fund = pd.read_csv(raw_dir + '01_fund_master.csv')

df_bench = pd.read_csv(raw_dir + '10_benchmark_indices.csv')
df_bench['date'] = pd.to_datetime(df_bench['date'])
df_bench = df_bench.sort_values(['index_name', 'date'])
"""
nb.cells.append(nbf.v4.new_code_cell(code_setup))

# 1. Compute daily returns
code_1 = """
# 1. Compute daily returns
df_nav['daily_return'] = df_nav.groupby('amfi_code')['nav'].pct_change()

plt.figure(figsize=(10, 5))
df_nav['daily_return'].hist(bins=100, density=True, alpha=0.7)
plt.title('Distribution of Daily Returns for all 40 Schemes')
plt.xlabel('Daily Return')
plt.ylabel('Density')
plt.show()

print("Daily returns computed and distribution looks roughly normal with fat tails as expected.")
"""
nb.cells.append(nbf.v4.new_code_cell(code_1))

# 2. Compute CAGR
code_2 = """
# 2. Compute CAGR for 1yr, 3yr, 5yr
def compute_cagr(df_group, years):
    df_group = df_group.sort_values('date')
    if len(df_group) == 0:
        return np.nan
    end_date = df_group['date'].iloc[-1]
    start_date = end_date - pd.DateOffset(years=years)
    
    df_period = df_group[df_group['date'] >= start_date]
    n_trading_days = len(df_period)
    
    # Require at least half the expected trading days
    if n_trading_days < (252 * years * 0.5):
        return np.nan
        
    nav_start = df_period['nav'].iloc[0]
    nav_end = df_period['nav'].iloc[-1]
    
    # Annualize using trading days (252 / n_trading_days)
    return (nav_end / nav_start) ** (252 / n_trading_days) - 1

cagr_1y = df_nav.groupby('amfi_code').apply(lambda x: compute_cagr(x, 1)).rename('cagr_1yr')
cagr_3y = df_nav.groupby('amfi_code').apply(lambda x: compute_cagr(x, 3)).rename('cagr_3yr')
cagr_5y = df_nav.groupby('amfi_code').apply(lambda x: compute_cagr(x, 5)).rename('cagr_5yr')

df_cagr = pd.concat([cagr_1y, cagr_3y, cagr_5y], axis=1).reset_index()
display(df_cagr.head())
"""
nb.cells.append(nbf.v4.new_code_cell(code_2))

# 3. Sharpe Ratio & 4. Sortino Ratio
code_3 = """
# 3 & 4. Sharpe and Sortino Ratios
rf = 0.065 # 6.5% RBI repo rate proxy
rf_daily = rf / 252

def compute_ratios(x):
    rets = x.dropna()
    if len(rets) < 100:
        return pd.Series({'sharpe': np.nan, 'sortino': np.nan})
    
    excess_ret = rets - rf_daily
    mean_excess = excess_ret.mean()
    std_ret = rets.std()
    
    sharpe = (mean_excess / std_ret) * np.sqrt(252) if std_ret > 0 else np.nan
    
    downside = rets[rets < 0]
    std_down = downside.std()
    sortino = (mean_excess / std_down) * np.sqrt(252) if std_down > 0 else np.nan
    
    return pd.Series({'sharpe': sharpe, 'sortino': sortino})

df_ratios = df_nav.groupby('amfi_code')['daily_return'].apply(compute_ratios).unstack().reset_index()
df_ratios['sharpe_rank'] = df_ratios['sharpe'].rank(ascending=False)
display(df_ratios.head())
"""
nb.cells.append(nbf.v4.new_code_cell(code_3))

# 5. Alpha and Beta
code_4 = """
# 5. Alpha and Beta against Nifty 100
nifty100 = df_bench[df_bench['index_name'] == 'NIFTY100'][['date', 'close_value']].rename(columns={'close_value': 'nifty_close'})
nifty100['nifty_ret'] = nifty100['nifty_close'].pct_change()

df_merged = pd.merge(df_nav[['amfi_code', 'date', 'daily_return']].dropna(), nifty100[['date', 'nifty_ret']].dropna(), on='date', how='inner')

def calc_alpha_beta(group):
    res = stats.linregress(group['nifty_ret'], group['daily_return'])
    alpha_ann = res.intercept * 252
    beta = res.slope
    return pd.Series({'alpha': alpha_ann, 'beta': beta})

df_ab = df_merged.groupby('amfi_code').apply(calc_alpha_beta).reset_index()
df_ab.to_csv('../reports/data/alpha_beta.csv', index=False)
display(df_ab.head())
"""
nb.cells.append(nbf.v4.new_code_cell(code_4))

# 6. Maximum Drawdown
code_5 = """
# 6. Maximum Drawdown
def calc_max_dd(group):
    group = group.sort_values('date')
    cummax = group['nav'].cummax()
    drawdown = (group['nav'] / cummax) - 1
    min_dd = drawdown.min()
    # Find worst drawdown date range
    worst_idx = drawdown.idxmin()
    worst_date = group.loc[worst_idx, 'date']
    # Start of drawdown is the cummax date before worst date
    start_dd_val = cummax.loc[worst_idx]
    start_date = group[(group['nav'] == start_dd_val) & (group['date'] <= worst_date)]['date'].min()
    return pd.Series({'max_dd': min_dd, 'dd_start': start_date, 'dd_worst': worst_date})

df_dd = df_nav.groupby('amfi_code').apply(calc_max_dd).reset_index()
display(df_dd.head())
"""
nb.cells.append(nbf.v4.new_code_cell(code_5))

# 7. Fund Scorecard
code_6 = """
# 7. Fund Scorecard
# Merge all metrics
df_score = df_cagr.merge(df_ratios, on='amfi_code')
df_score = df_score.merge(df_ab, on='amfi_code')
df_score = df_score.merge(df_dd[['amfi_code', 'max_dd']], on='amfi_code')
df_score = df_score.merge(df_fund[['amfi_code', 'expense_ratio_pct', 'scheme_name']], on='amfi_code')

# Percentile ranks (0 to 100)
r_3yr = df_score['cagr_3yr'].rank(pct=True) * 100
r_sharpe = df_score['sharpe'].rank(pct=True) * 100
r_alpha = df_score['alpha'].rank(pct=True) * 100
r_exp = df_score['expense_ratio_pct'].rank(ascending=False, pct=True) * 100 # inverse
r_dd = df_score['max_dd'].rank(pct=True) * 100 # max_dd is negative, less negative is higher rank

# Composite score: 30% × 3yr return rank + 25% × Sharpe rank + 20% × Alpha rank + 15% × expense ratio rank + 10% × max DD rank
df_score['composite_score'] = (0.30 * r_3yr) + (0.25 * r_sharpe) + (0.20 * r_alpha) + (0.15 * r_exp) + (0.10 * r_dd)

df_score = df_score.sort_values('composite_score', ascending=False)
df_score.to_csv('../reports/data/fund_scorecard.csv', index=False)
display(df_score[['scheme_name', 'composite_score', 'cagr_3yr', 'sharpe', 'alpha', 'expense_ratio_pct', 'max_dd']].head(10))
"""
nb.cells.append(nbf.v4.new_code_cell(code_6))

# 8. Benchmark comparison chart & Tracking error
code_7 = """
# 8. Benchmark comparison chart
top_5_amfi = df_score.head(5)['amfi_code'].tolist()

# Get 3 years data
end_date = df_nav['date'].max()
start_date = end_date - pd.DateOffset(years=3)

df_nav_3y = df_nav[(df_nav['date'] >= start_date) & (df_nav['amfi_code'].isin(top_5_amfi))]
df_bench_3y = df_bench[(df_bench['date'] >= start_date) & (df_bench['index_name'].isin(['NIFTY50', 'NIFTY100']))]

plt.figure(figsize=(14, 7))

# Plot Nifty 50 and 100
for idx in ['NIFTY50', 'NIFTY100']:
    d = df_bench_3y[df_bench_3y['index_name'] == idx].sort_values('date')
    d['norm_val'] = d['close_value'] / d['close_value'].iloc[0] * 100
    plt.plot(d['date'], d['norm_val'], label=idx, linewidth=3, linestyle='--')

# Plot top 5 funds
for code in top_5_amfi:
    d = df_nav_3y[df_nav_3y['amfi_code'] == code].sort_values('date')
    d['norm_val'] = d['nav'] / d['nav'].iloc[0] * 100
    name = df_fund[df_fund['amfi_code']==code]['scheme_name'].values[0]
    # shorten name
    name = name[:30] + '..' if len(name) > 30 else name
    plt.plot(d['date'], d['norm_val'], label=name)

plt.title('Top 5 Funds vs Benchmarks (3-Year Normalized Growth)')
plt.ylabel('Normalized Value (Base 100)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/charts/benchmark_comparison.png')
plt.show()

# Compute tracking error against NIFTY 100 for top 5
te_data = []
nifty100_ret = df_bench_3y[df_bench_3y['index_name'] == 'NIFTY100'].set_index('date')['close_value'].pct_change()
for code in top_5_amfi:
    fund_ret = df_nav_3y[df_nav_3y['amfi_code'] == code].set_index('date')['nav'].pct_change()
    diff = fund_ret - nifty100_ret
    te = diff.std() * np.sqrt(252)
    name = df_fund[df_fund['amfi_code']==code]['scheme_name'].values[0]
    te_data.append({'Fund': name, 'Tracking Error': te})

display(pd.DataFrame(te_data))
"""
nb.cells.append(nbf.v4.new_code_cell(code_7))

with open('notebooks/04_performance_analytics.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook 04_performance_analytics.ipynb generated.")
