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

st.sidebar.header('Filters')

ticker_list = st.sidebar.multiselect('Choose your shares', datas.columns)
if ticker_list:
    datas = datas[ticker_list]
    if len(ticker_list) == 1:
        stock = ticker_list[0]
        datas = datas.rename(columns={stock: 'Close'})

start_date = datas.index.min().to_pydatetime()
end_date = datas.index.max().to_pydatetime()
interval_date = st.sidebar.slider('Filter a time interval', min_value=start_date, max_value=end_date, 
                  value=(start_date, end_date))

datas = datas.loc[interval_date[0]:interval_date[1]]


st.line_chart(datas)