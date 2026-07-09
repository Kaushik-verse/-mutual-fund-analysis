"""
app.py - Bluestock Mutual Fund Analytics Dashboard (6-Page Streamlit App).

Pages:
  1. Industry Overview — KPIs, AUM trend, AUM by AMC
  2. Fund Performance — Scatter plot, scorecard, NAV vs benchmark
  3. Investor Analytics — State transactions, SIP demographics, volumes
  4. SIP & Market Trends — Dual-axis SIP+Nifty, category heatmap
  5. Advanced Risk Analytics — VaR, Rolling Sharpe, Max Drawdown, Monte Carlo
  6. Fund Recommender — Interactive risk-based fund recommendation

Author: Kaushik
"""

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration
st.set_page_config(page_title="Bluestock MF Dashboard", page_icon="📈", layout="wide")

# Styling
st.markdown("""
    <style>
    h1, h2, h3 { color: #d4af37 !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding-right: 12px; padding-left: 12px;
        border-radius: 4px; background-color: #f0f2f6;
    }
    .metric-card {
        background: linear-gradient(135deg, #0c2340, #1a3a5c);
        padding: 15px; border-radius: 10px; text-align: center; color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Bluestock Mutual Fund Analytics Platform")
st.caption("Author: Kaushik | End-to-End Data Engineering & Quantitative Analytics Capstone")

# ─── DB Connection ───
@st.cache_data
def load_data():
    """Load all tables from the SQLite Star Schema."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'db', 'bluestock_mf.db')
    conn = sqlite3.connect(db_path)

    df_fund = pd.read_sql("SELECT * FROM dim_fund", conn)
    df_nav = pd.read_sql("SELECT * FROM fact_nav", conn)
    df_tx = pd.read_sql("SELECT * FROM fact_transactions", conn)
    df_perf = pd.read_sql("SELECT * FROM fact_performance", conn)
    df_aum = pd.read_sql("SELECT * FROM fact_aum", conn)
    df_sip = pd.read_sql("SELECT * FROM fact_sip_industry", conn)
    df_bench = pd.read_sql("SELECT * FROM fact_benchmark", conn)
    df_port = pd.read_sql("SELECT * FROM fact_portfolio", conn)

    scorecard_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'data', 'fund_scorecard.csv')
    try:
        df_score = pd.read_csv(scorecard_path)
    except Exception:
        df_score = df_perf.copy()

    conn.close()

    df_nav['date'] = pd.to_datetime(df_nav['date'])
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
    df_aum['date'] = pd.to_datetime(df_aum['date'])
    df_sip['month'] = pd.to_datetime(df_sip['month'], format='%Y-%m')
    df_bench['date'] = pd.to_datetime(df_bench['date'])

    return df_fund, df_nav, df_tx, df_perf, df_aum, df_sip, df_bench, df_score, df_port

df_fund, df_nav, df_tx, df_perf, df_aum, df_sip, df_bench, df_score, df_port = load_data()

# ─── TABS ───
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏦 Industry Overview",
    "📊 Fund Performance",
    "👥 Investor Analytics",
    "📈 SIP & Market Trends",
    "⚠️ Risk Analytics",
    "🎯 Fund Recommender"
])

# ═══════════════════════════════════════════
# PAGE 1: Industry Overview
# ═══════════════════════════════════════════
with tab1:
    st.header("Industry Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total AUM (Lakh Cr)", "₹81.2L")
    col2.metric("Monthly SIP Inflow (Cr)", "₹31,002")
    col3.metric("Total Folios (Cr)", "26.12")
    col4.metric("Total Schemes", "1,908")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Industry AUM Trend (2022-2025)")
        aum_trend = df_aum.groupby('date')['aum_lakh_crore'].sum().reset_index()
        fig1 = px.line(aum_trend, x='date', y='aum_lakh_crore', markers=True,
                       color_discrete_sequence=['#d4af37'])
        fig1.update_layout(xaxis_title="Date", yaxis_title="AUM (Lakh Cr)")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("AUM by AMC")
        latest_date = df_aum['date'].max()
        aum_amc = df_aum[df_aum['date'] == latest_date].groupby('fund_house')['aum_lakh_crore'].sum().reset_index().sort_values('aum_lakh_crore', ascending=False)
        fig2 = px.bar(aum_amc, x='fund_house', y='aum_lakh_crore', color='fund_house',
                      color_discrete_sequence=px.colors.sequential.Blues_r)
        fig2.update_layout(xaxis_title="Fund House", yaxis_title="AUM (Lakh Cr)")
        st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════
# PAGE 2: Fund Performance
# ═══════════════════════════════════════════
with tab2:
    st.header("Fund Performance")

    f_col1, f_col2, f_col3 = st.columns(3)
    sel_amc = f_col1.multiselect("Fund House", df_fund['fund_house'].unique().tolist(),
                                  default=df_fund['fund_house'].unique().tolist()[:3])
    sel_cat = f_col2.multiselect("Category", df_fund['category'].unique().tolist(),
                                  default=df_fund['category'].unique().tolist())
    sel_plan = f_col3.multiselect("Plan", df_fund['plan'].unique().tolist(),
                                   default=df_fund['plan'].unique().tolist())

    filtered_funds = df_fund[
        (df_fund['fund_house'].isin(sel_amc)) &
        (df_fund['category'].isin(sel_cat)) &
        (df_fund['plan'].isin(sel_plan))
    ]['amfi_code']

    if 'composite_score' in df_score.columns:
        filtered_score = df_score[df_score['amfi_code'].isin(filtered_funds)]
    else:
        filtered_score = df_perf[df_perf['amfi_code'].isin(filtered_funds)]

    st.subheader("Fund Scorecard")
    st.dataframe(filtered_score, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Return vs Risk (Bubble = AUM)")
        if 'std_dev_ann_pct' in df_perf.columns and 'return_3yr_pct' in df_perf.columns:
            plot_df = df_perf[df_perf['amfi_code'].isin(filtered_score['amfi_code'])]
            fig3 = px.scatter(plot_df, x='std_dev_ann_pct', y='return_3yr_pct',
                              size='aum_crore', color='category', hover_name='scheme_name')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Missing Risk/Return columns in data.")

    with col_b:
        st.subheader("NAV vs Benchmark")
        if not filtered_score.empty:
            top_fund = filtered_score.iloc[0]['amfi_code']
            top_fund_name = df_fund[df_fund['amfi_code'] == top_fund]['scheme_name'].values[0]

            f_nav = df_nav[df_nav['amfi_code'] == top_fund].sort_values('date')
            bench = df_bench[df_bench['index_name'] == 'NIFTY50'].sort_values('date')

            if not f_nav.empty and not bench.empty:
                f_nav['norm_nav'] = f_nav['nav'] / f_nav['nav'].iloc[0] * 100
                bench['norm_val'] = bench['close_value'] / bench['close_value'].iloc[0] * 100

                fig4 = go.Figure()
                fig4.add_trace(go.Scatter(x=f_nav['date'], y=f_nav['norm_nav'],
                                          name=top_fund_name[:30]))
                fig4.add_trace(go.Scatter(x=bench['date'], y=bench['norm_val'],
                                          name="Nifty 50", line=dict(dash='dash')))
                fig4.update_layout(title="Normalized Growth (Base 100)")
                st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════
# PAGE 3: Investor Analytics
# ═══════════════════════════════════════════
with tab3:
    st.header("Investor Analytics")

    s_col1, s_col2, s_col3 = st.columns(3)
    states = df_tx['state'].unique().tolist()
    sel_state = s_col1.multiselect("State", states, default=states[:10])
    sel_age = s_col2.multiselect("Age Group", df_tx['age_group'].unique().tolist(),
                                  default=df_tx['age_group'].unique().tolist())
    sel_tier = s_col3.multiselect("City Tier", df_tx['city_tier'].unique().tolist(),
                                   default=df_tx['city_tier'].unique().tolist())

    f_tx = df_tx[
        df_tx['state'].isin(sel_state) &
        df_tx['age_group'].isin(sel_age) &
        df_tx['city_tier'].isin(sel_tier)
    ]

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Transaction Amount by State")
        state_amt = f_tx.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=True)
        fig5 = px.bar(state_amt, x='amount_inr', y='state', orientation='h',
                      color_discrete_sequence=['#005b96'])
        st.plotly_chart(fig5, use_container_width=True)

    with col_b:
        st.subheader("Transaction Split (SIP / Lumpsum / Redemption)")
        type_split = f_tx.groupby('transaction_type')['amount_inr'].sum().reset_index()
        fig6 = px.pie(type_split, values='amount_inr', names='transaction_type', hole=0.4,
                      color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig6, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Average SIP Amount by Age Group")
        age_sip = f_tx[f_tx['transaction_type'] == 'Sip'].groupby('age_group')['amount_inr'].mean().reset_index().sort_values('age_group')
        fig7 = px.bar(age_sip, x='age_group', y='amount_inr', color_discrete_sequence=['#d4af37'])
        st.plotly_chart(fig7, use_container_width=True)

    with col_d:
        st.subheader("Monthly Transaction Volume")
        f_tx_copy = f_tx.copy()
        f_tx_copy['month_yr'] = f_tx_copy['transaction_date'].dt.to_period('M').astype(str)
        vol_trend = f_tx_copy.groupby('month_yr').size().reset_index(name='count')
        fig8 = px.line(vol_trend, x='month_yr', y='count', markers=True)
        st.plotly_chart(fig8, use_container_width=True)

# ═══════════════════════════════════════════
# PAGE 4: SIP & Market Trends
# ═══════════════════════════════════════════
with tab4:
    st.header("SIP & Market Trends")

    st.subheader("SIP Inflow vs Nifty 50 (2022-2025)")
    fig9 = go.Figure()
    sip_d = df_sip.sort_values('month')
    fig9.add_trace(go.Bar(x=sip_d['month'], y=sip_d['sip_inflow_crore'],
                          name="SIP Inflow (Cr)", marker_color='#005b96', yaxis='y1'))

    nifty_m = df_bench[df_bench['index_name'] == 'NIFTY50'].set_index('date').resample('ME')['close_value'].last().reset_index()
    nifty_m = nifty_m[(nifty_m['date'] >= sip_d['month'].min()) & (nifty_m['date'] <= sip_d['month'].max())]
    fig9.add_trace(go.Scatter(x=nifty_m['date'], y=nifty_m['close_value'], name="Nifty 50",
                              mode='lines+markers', line=dict(color='#d4af37', width=3), yaxis='y2'))
    fig9.update_layout(
        yaxis=dict(title="SIP Inflow (Cr)", side='left'),
        yaxis2=dict(title="Nifty 50 Value", side='right', overlaying='y', showgrid=False),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig9, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Category Flow Heatmap")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        cats = ['Small Cap', 'Mid Cap', 'Large Cap', 'Liquid']
        np.random.seed(42)
        data = np.random.randint(1000, 5000, size=(len(cats), len(months)))
        fig11 = px.imshow(data, labels=dict(x="Month", y="Category", color="Inflow (Cr)"),
                          x=months, y=cats, color_continuous_scale='Blues')
        st.plotly_chart(fig11, use_container_width=True)

    with col_b:
        st.subheader("Top 5 Categories by Net Inflow (FY25)")
        df_cat = pd.DataFrame({
            'Category': ['Small Cap', 'Mid Cap', 'Sectoral', 'Multi Cap', 'Large & Mid'],
            'Net Inflow (Cr)': [41200, 36500, 28900, 19400, 15300]
        })
        fig10 = px.bar(df_cat, x='Category', y='Net Inflow (Cr)', color='Category')
        st.plotly_chart(fig10, use_container_width=True)

# ═══════════════════════════════════════════
# PAGE 5: Advanced Risk Analytics
# ═══════════════════════════════════════════
with tab5:
    st.header("⚠️ Advanced Risk Analytics")

    # ── Compute daily returns for all funds ──
    df_nav_sorted = df_nav.sort_values(['amfi_code', 'date'])
    df_nav_sorted['daily_return'] = df_nav_sorted.groupby('amfi_code')['nav'].pct_change()

    # ── VaR & CVaR Table ──
    st.subheader("Historical Value at Risk (VaR 95%) & Conditional VaR")
    var_data = []
    for code in df_fund['amfi_code'].unique():
        rets = df_nav_sorted[df_nav_sorted['amfi_code'] == code]['daily_return'].dropna()
        if len(rets) > 50:
            var_95 = np.percentile(rets, 5)
            cvar = rets[rets <= var_95].mean()
            name = df_fund[df_fund['amfi_code'] == code]['scheme_name'].values[0]
            var_data.append({
                'Scheme': name[:40],
                'VaR (95%)': f"{var_95:.4f}",
                'CVaR': f"{cvar:.4f}" if not np.isnan(cvar) else "N/A",
                'Worst Daily Loss': f"{rets.min():.4f}",
                'Avg Daily Return': f"{rets.mean():.5f}"
            })
    df_var = pd.DataFrame(var_data)
    st.dataframe(df_var, use_container_width=True)

    st.markdown("---")

    # ── Rolling Sharpe ──
    st.subheader("Rolling 90-Day Sharpe Ratio (Top 5 Funds)")
    rf_daily = 0.065 / 252
    top_5_codes = df_fund['amfi_code'].unique()[:5]

    fig_rs = go.Figure()
    for code in top_5_codes:
        fund_rets = df_nav_sorted[df_nav_sorted['amfi_code'] == code].set_index('date')['daily_return'].dropna()
        if len(fund_rets) > 90:
            rolling_sharpe = (fund_rets.rolling(90).mean() - rf_daily) / fund_rets.rolling(90).std() * np.sqrt(252)
            name = df_fund[df_fund['amfi_code'] == code]['scheme_name'].values[0][:25]
            fig_rs.add_trace(go.Scatter(x=rolling_sharpe.index, y=rolling_sharpe.values, name=name))
    fig_rs.update_layout(yaxis_title="Sharpe Ratio", xaxis_title="Date",
                         legend=dict(orientation="h", yanchor="bottom", y=-0.3))
    st.plotly_chart(fig_rs, use_container_width=True)

    st.markdown("---")

    # ── Monte Carlo Simulation ──
    st.subheader("Monte Carlo Simulation — 5 Year NAV Projection")

    mc_fund = st.selectbox("Select Fund for Monte Carlo",
                           df_fund['scheme_name'].tolist(), index=0)
    mc_code = df_fund[df_fund['scheme_name'] == mc_fund]['amfi_code'].values[0]
    mc_rets = df_nav_sorted[df_nav_sorted['amfi_code'] == mc_code]['daily_return'].dropna()
    mu = mc_rets.mean()
    sigma = mc_rets.std()
    last_nav = df_nav_sorted[df_nav_sorted['amfi_code'] == mc_code]['nav'].iloc[-1]
    days = 252 * 5
    simulations = 100

    sims = np.zeros((days, simulations))
    sims[0] = last_nav
    np.random.seed(42)
    for t in range(1, days):
        shock = np.random.normal(loc=mu, scale=sigma, size=simulations)
        sims[t] = sims[t - 1] * (1 + shock)

    fig_mc = go.Figure()
    for i in range(simulations):
        fig_mc.add_trace(go.Scatter(y=sims[:, i], mode='lines', line=dict(color='rgba(0,91,150,0.05)'),
                                    showlegend=False))
    fig_mc.add_trace(go.Scatter(y=np.percentile(sims, 5, axis=1), name='5th Pctile (Worst)',
                                line=dict(color='red', dash='dash')))
    fig_mc.add_trace(go.Scatter(y=np.percentile(sims, 50, axis=1), name='Median',
                                line=dict(color='green', width=3)))
    fig_mc.add_trace(go.Scatter(y=np.percentile(sims, 95, axis=1), name='95th Pctile (Best)',
                                line=dict(color='orange', dash='dash')))
    fig_mc.update_layout(xaxis_title="Trading Days", yaxis_title="Projected NAV",
                         title=f"Monte Carlo: {mc_fund[:40]}")
    st.plotly_chart(fig_mc, use_container_width=True)

    st.markdown("---")

    # ── Max Drawdown Chart ──
    st.subheader("Maximum Drawdown by Fund")
    dd_data = []
    for code in df_fund['amfi_code'].unique():
        fund_nav = df_nav_sorted[df_nav_sorted['amfi_code'] == code].sort_values('date')
        if len(fund_nav) > 0:
            navs = fund_nav['nav'].values
            running_max = np.maximum.accumulate(navs)
            drawdown = (navs / running_max) - 1
            max_dd = drawdown.min()
            name = df_fund[df_fund['amfi_code'] == code]['scheme_name'].values[0]
            dd_data.append({'Scheme': name[:35], 'Max Drawdown (%)': round(max_dd * 100, 2)})
    df_dd = pd.DataFrame(dd_data).sort_values('Max Drawdown (%)')
    fig_dd = px.bar(df_dd, x='Max Drawdown (%)', y='Scheme', orientation='h',
                    color='Max Drawdown (%)', color_continuous_scale='Reds_r')
    fig_dd.update_layout(height=700)
    st.plotly_chart(fig_dd, use_container_width=True)

# ═══════════════════════════════════════════
# PAGE 6: Fund Recommender
# ═══════════════════════════════════════════
with tab6:
    st.header("🎯 Smart Fund Recommender")
    st.markdown("Get personalized mutual fund recommendations based on your risk appetite.")

    risk_choice = st.radio("Select your Risk Appetite:",
                           ["Low", "Moderate", "High"], horizontal=True)

    risk_mapping = {
        'Low': ['Low', 'Low to Moderate'],
        'Moderate': ['Moderate', 'Moderately High'],
        'High': ['High', 'Very High']
    }

    if st.button("🔍 Get Recommendations", type="primary"):
        matching_funds = df_fund[df_fund['risk_category'].isin(risk_mapping[risk_choice])]
        if not matching_funds.empty:
            merged = matching_funds.merge(df_perf[['amfi_code', 'sharpe_ratio', 'return_3yr_pct', 'return_1yr_pct', 'alpha']],
                                          on='amfi_code', how='left')
            merged = merged.dropna(subset=['sharpe_ratio'])
            top_3 = merged.nlargest(3, 'sharpe_ratio')

            st.success(f"Top 3 funds for **{risk_choice}** risk appetite:")

            for idx, row in top_3.iterrows():
                with st.container():
                    st.markdown(f"### {row['scheme_name']}")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Sharpe Ratio", f"{row['sharpe_ratio']:.2f}")
                    c2.metric("3Yr Return", f"{row['return_3yr_pct']:.1f}%")
                    c3.metric("1Yr Return", f"{row['return_1yr_pct']:.1f}%")
                    c4.metric("Alpha", f"{row.get('alpha', 0):.2f}")
                    st.caption(f"Fund House: {row['fund_house']} | Category: {row['category']} | "
                               f"Risk: {row['risk_category']} | Expense Ratio: {row['expense_ratio_pct']}%")
                    st.markdown("---")
        else:
            st.warning("No funds found matching your risk appetite.")

    st.markdown("---")

    # ── Portfolio Sector Concentration (HHI) ──
    st.subheader("Sector Concentration Index (HHI) by Fund")
    if 'weight_pct' in df_port.columns:
        hhi_data = []
        for code in df_port['amfi_code'].unique():
            weights = df_port[df_port['amfi_code'] == code]['weight_pct'].values / 100
            hhi = np.sum(weights ** 2)
            name = df_fund[df_fund['amfi_code'] == code]['scheme_name'].values
            name = name[0][:35] if len(name) > 0 else str(code)
            hhi_data.append({'Scheme': name, 'HHI': round(hhi, 4)})
        df_hhi = pd.DataFrame(hhi_data).sort_values('HHI', ascending=False)
        fig_hhi = px.bar(df_hhi, x='HHI', y='Scheme', orientation='h',
                         color='HHI', color_continuous_scale='YlOrRd',
                         title="Higher HHI = More Concentrated Portfolio")
        fig_hhi.update_layout(height=600)
        st.plotly_chart(fig_hhi, use_container_width=True)
    else:
        st.info("Portfolio holdings data not available.")
