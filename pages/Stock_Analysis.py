import os
import sys
import streamlit as st
import pandas as pd 
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta

if __package__ is None or __package__ == "":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

from pages.utils.plotly_figure import plotly_table

# setting page config
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide",
)

st.title("Stock Analysis")

col1, col2, col3, =st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)
info = stock.info

st.write(info.get('longBusinessSummary', 'Business summary unavailable.'))
st.write(info.get('sector', 'Sector unavailable.'))
st.write(info.get('fullTimeEmployees', 'Employee count unavailable.'))
st.write(info.get('website', 'Website unavailable.'))

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index = ['Market Cap','Beta','EPS','PE Ratio'])
    df['']= [stock.info["marketCap"],stock.info["beta"],stock.info["trailingEps"],stock.info["trailingPE"]]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, width='stretch')
with col2:
    df = pd.DataFrame(index = ['Quick Ratio','Revenue per share','Profit Margins',
                               'Debt to Equity','Return on Equity'])
    df[''] = [stock.info["quickRatio"],stock.info["revenuePerShare"],stock.info["profitMargins"],stock.info["debtToEquity"],stock.info["returnOnEquity"]]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, width="stretch")

data = yf.download(ticker, start=start_date, end=end_date)

if len(data) >= 2 and 'Close' in data.columns:
    try:
        last_close = float(data['Close'].iloc[-1])
        prev_close = float(data['Close'].iloc[-2])
    except (TypeError, ValueError):
        last_close = None
        prev_close = None

    if last_close is not None and prev_close is not None:
        col1, col2, col3 = st.columns(3)
        daily_change = last_close - prev_close
        col1.metric("Daily Change", str(round(last_close, 2)), str(round(daily_change, 2)))

data.tail(10).sort_index(ascending=False)