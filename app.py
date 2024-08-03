import streamlit as st
import pandas as pd
import yfinance as yf


@st.cache_data
def loading_data(ticker_list):
    tickers = ' '.join(ticker_list)
    data_stock = yf.Tickers(tickers)
    quotation_stock = data_stock.history(period='1d', start='2000-01-01', end='2023-12-31')
    return quotation_stock['Close']

ticker_list = ['AAPL', 'MSFT', 'INTC', 'AMZN', 'C', 'AXP', 'F', 'MS']
datas = loading_data(ticker_list)

st.write('''
# App prices of stocks
''')

ticker_list = st.multiselect('Choose your shares', datas.columns)
if ticker_list:
    datas = datas[ticker_list]
    if len(ticker_list) == 1:
        stock = ticker_list[0]
        datas = datas.rename(columns={stock: 'Close'})

st.line_chart(datas)