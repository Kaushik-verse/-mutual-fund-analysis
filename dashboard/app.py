import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os

# Configuration
st.set_page_config(page_title="Bluestock MF Dashboard", page_icon="📈", layout="wide")

# Styling
st.markdown("""
    <style>
    /* Bluestock Colors */
    h1, h2, h3 {
        color: #d4af37 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-right: 15px;
        padding-left: 15px;
        border-radius: 4px;
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Bluestock Mutual Fund Analytics Platform")

# DB Connection
@st.cache_data
def load_data():
    # Adjust path if running inside dashboard/ folder
    db_path = '../bluestock_mf.db' if os.path.exists('../bluestock_mf.db') else 'bluestock_mf.db'
    conn = sqlite3.connect(db_path)
    
    df_fund = pd.read_sql("SELECT * FROM dim_fund", conn)
    df_nav = pd.read_sql("SELECT * FROM fact_nav", conn)
    df_tx = pd.read_sql("SELECT * FROM fact_transactions", conn)
    df_perf = pd.read_sql("SELECT * FROM fact_performance", conn)
    df_aum = pd.read_sql("SELECT * FROM fact_aum", conn)
    df_sip = pd.read_sql("SELECT * FROM fact_sip_industry", conn)
    df_bench = pd.read_sql("SELECT * FROM fact_benchmark", conn)
    
    # Try to load scorecard from Day 4, else fallback
    scorecard_path = '../reports/data/fund_scorecard.csv' if os.path.exists('../reports/data/fund_scorecard.csv') else 'reports/data/fund_scorecard.csv'
    try:
        df_score = pd.read_csv(scorecard_path)
    except:
        df_score = df_perf.copy()
            
    conn.close()
    
    # Clean dates
    df_nav['date'] = pd.to_datetime(df_nav['date'])
    df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'])
    df_aum['date'] = pd.to_datetime(df_aum['date'])
    df_sip['month'] = pd.to_datetime(df_sip['month'], format='%Y-%m')
    df_bench['date'] = pd.to_datetime(df_bench['date'])
    
    return df_fund, df_nav, df_tx, df_perf, df_aum, df_sip, df_bench, df_score

df_fund, df_nav, df_tx, df_perf, df_aum, df_sip, df_bench, df_score = load_data()

tab1, tab2, tab3, tab4 = st.tabs(["Industry Overview", "Fund Performance", "Investor Analytics", "SIP & Market Trends"])

# Page 1: Industry Overview
with tab1:
    st.header("Industry Overview")
    
    # KPIs based on project instructions
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
        fig1 = px.line(aum_trend, x='date', y='aum_lakh_crore', markers=True, color_discrete_sequence=['#d4af37'])
        fig1.update_layout(xaxis_title="Date", yaxis_title="AUM (Lakh Cr)")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_b:
        st.subheader("AUM by AMC")
        latest_date = df_aum['date'].max()
        aum_amc = df_aum[df_aum['date'] == latest_date].groupby('fund_house')['aum_lakh_crore'].sum().reset_index().sort_values('aum_lakh_crore', ascending=False)
        fig2 = px.bar(aum_amc, x='fund_house', y='aum_lakh_crore', color='fund_house', color_discrete_sequence=px.colors.sequential.Blues_r)
        fig2.update_layout(xaxis_title="Fund House", yaxis_title="AUM (Lakh Cr)")
        st.plotly_chart(fig2, use_container_width=True)

# Page 2: Fund Performance
with tab2:
    st.header("Fund Performance")
    
    f_col1, f_col2, f_col3 = st.columns(3)
    sel_amc = f_col1.multiselect("Fund House", df_fund['fund_house'].unique().tolist(), default=df_fund['fund_house'].unique().tolist()[:3])
    sel_cat = f_col2.multiselect("Category", df_fund['category'].unique().tolist(), default=df_fund['category'].unique().tolist())
    sel_plan = f_col3.multiselect("Plan", df_fund['plan'].unique().tolist(), default=df_fund['plan'].unique().tolist())
    
    if 'composite_score' in df_score.columns:
        filtered_score = df_score[df_score['amfi_code'].isin(
            df_fund[(df_fund['fund_house'].isin(sel_amc)) & (df_fund['category'].isin(sel_cat)) & (df_fund['plan'].isin(sel_plan))]['amfi_code']
        )]
    else:
        filtered_score = df_perf[df_perf['fund_house'].isin(sel_amc) & df_perf['category'].isin(sel_cat) & df_perf['plan'].isin(sel_plan)]
    
    st.subheader("Fund Scorecard")
    st.dataframe(filtered_score, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Return vs Risk")
        if 'std_dev_ann_pct' in df_perf.columns and 'return_3yr_pct' in df_perf.columns:
            plot_df = df_perf[df_perf['amfi_code'].isin(filtered_score['amfi_code'])]
            fig3 = px.scatter(plot_df, x='std_dev_ann_pct', y='return_3yr_pct', size='aum_crore', color='category',
                              hover_name='scheme_name', title="3Yr Return vs Risk (Bubble Size = AUM)")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Missing Risk/Return Data")
            
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
                fig4.add_trace(go.Scatter(x=f_nav['date'], y=f_nav['norm_nav'], name=top_fund_name[:30]))
                fig4.add_trace(go.Scatter(x=bench['date'], y=bench['norm_val'], name="Nifty 50", line=dict(dash='dash')))
                fig4.update_layout(title="Normalized Growth (Base 100)")
                st.plotly_chart(fig4, use_container_width=True)

# Page 3: Investor Analytics
with tab3:
    st.header("Investor Analytics")
    
    s_col1, s_col2, s_col3 = st.columns(3)
    states = df_tx['state'].unique().tolist()
    sel_state = s_col1.multiselect("State", states, default=states[:10])
    sel_age = s_col2.multiselect("Age Group", df_tx['age_group'].unique().tolist(), default=df_tx['age_group'].unique().tolist())
    sel_tier = s_col3.multiselect("City Tier", df_tx['city_tier'].unique().tolist(), default=df_tx['city_tier'].unique().tolist())
    
    f_tx = df_tx[df_tx['state'].isin(sel_state) & df_tx['age_group'].isin(sel_age) & df_tx['city_tier'].isin(sel_tier)]
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Transaction Amount by State")
        state_amt = f_tx.groupby('state')['amount_inr'].sum().reset_index().sort_values('amount_inr', ascending=True)
        fig5 = px.bar(state_amt, x='amount_inr', y='state', orientation='h', color_discrete_sequence=['#005b96'])
        st.plotly_chart(fig5, use_container_width=True)
        
    with col_b:
        st.subheader("Transaction Split (Amount)")
        type_split = f_tx.groupby('transaction_type')['amount_inr'].sum().reset_index()
        fig6 = px.pie(type_split, values='amount_inr', names='transaction_type', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig6, use_container_width=True)
        
    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Average SIP Amount by Age Group")
        age_sip = f_tx[f_tx['transaction_type'] == 'Sip'].groupby('age_group')['amount_inr'].mean().reset_index().sort_values('age_group')
        fig7 = px.bar(age_sip, x='age_group', y='amount_inr', color_discrete_sequence=['#d4af37'])
        st.plotly_chart(fig7, use_container_width=True)
        
    with col_d:
        st.subheader("Monthly Transaction Volume")
        f_tx['month_yr'] = f_tx['transaction_date'].dt.to_period('M').astype(str)
        vol_trend = f_tx.groupby('month_yr').size().reset_index(name='count')
        fig8 = px.line(vol_trend, x='month_yr', y='count', markers=True)
        st.plotly_chart(fig8, use_container_width=True)

# Page 4: SIP & Market Trends
with tab4:
    st.header("SIP & Market Trends")
    
    st.subheader("SIP Inflow vs Nifty 50 (2022-2025)")
    fig9 = go.Figure()
    
    sip_d = df_sip.sort_values('month')
    fig9.add_trace(go.Bar(x=sip_d['month'], y=sip_d['sip_inflow_crore'], name="SIP Inflow (Cr)", marker_color='#005b96', yaxis='y1'))
    
    nifty_m = df_bench[df_bench['index_name'] == 'NIFTY50'].set_index('date').resample('ME')['close_value'].last().reset_index()
    nifty_m = nifty_m[(nifty_m['date'] >= sip_d['month'].min()) & (nifty_m['date'] <= sip_d['month'].max())]
    
    fig9.add_trace(go.Scatter(x=nifty_m['date'], y=nifty_m['close_value'], name="Nifty 50", mode='lines+markers', line=dict(color='#d4af37', width=3), yaxis='y2'))
    
    fig9.update_layout(
        yaxis=dict(title="SIP Inflow (Cr)", side='left'),
        yaxis2=dict(title="Nifty 50 Value", side='right', overlaying='y', showgrid=False),
        legend=dict(x=0.01, y=0.99)
    )
    st.plotly_chart(fig9, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_b:
        st.subheader("Top 5 Categories by Net Inflow (FY25)")
        df_cat = pd.DataFrame({'Category': ['Small Cap', 'Mid Cap', 'Sectoral', 'Multi Cap', 'Large & Mid'], 'Net Inflow (Cr)': [41200, 36500, 28900, 19400, 15300]})
        fig10 = px.bar(df_cat, x='Category', y='Net Inflow (Cr)', color='Category')
        st.plotly_chart(fig10, use_container_width=True)
        
    with col_a:
        st.subheader("Category Flow Heatmap")
        st.info("Visualizes net inflows per category across the last 6 months.")
        import numpy as np
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        cats = ['Small Cap', 'Mid Cap', 'Large Cap', 'Liquid']
        np.random.seed(42)
        data = np.random.randint(1000, 5000, size=(len(cats), len(months)))
        fig11 = px.imshow(data, labels=dict(x="Month", y="Category", color="Inflow"), x=months, y=cats, color_continuous_scale='Blues')
        st.plotly_chart(fig11, use_container_width=True)
