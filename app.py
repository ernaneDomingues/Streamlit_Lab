import streamlit as st
import pandas as pd
import yfinance as yf


# @st.cache_data
# def loading_data(ticker_list):
#     tickers = ' '.join(ticker_list)
#     data_stock = yf.Tickers(tickers)
#     quotation_stock = data_stock.history(period='1d', start='2000-01-01', end='2023-12-31')
#     return quotation_stock['Close']

@st.cache_data
def loading_data(ticker_list):
    data_stock = yf.download(ticker_list, start='1900-01-01', period='1d')
    return data_stock['Close']

def loading_tickers():
    tickers = pd.read_csv('IBOVDia_12-08-24.csv', sep=';').reset_index()
    tickers = list(tickers['index'])
    tickers = [ticker + '.SA' for ticker in tickers]
    return tickers

tickers_list = loading_tickers()
# print(tickers_list)
# ticker_list = ['AAPL', 'MSFT', 'INTC', 'AMZN', 'C', 'AXP', 'F', 'MS']
# datas = loading_data(tickers_list)

datas = loading_data(tickers_list)

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

performance_stock_text = ''

if len(ticker_list)==0:
    ticker_list = list(datas.columns)
elif len(ticker_list)==1:
    datas = datas.rename(columns={'Close': stock} )

stock_portfolio = [1000 for stock in ticker_list]
stock_portfolio_total_start = sum(stock_portfolio)

for i, stock in enumerate(ticker_list):
    performance_stock = float(datas[stock].iloc[-1] / datas[stock].iloc[0] - 1)

    stock_portfolio[i] = stock_portfolio[i] * (1 + performance_stock)

    if performance_stock > 0:
        performance_stock_text = performance_stock_text + f'  \n{stock}: :green[{performance_stock:.2%}]'
    elif performance_stock < 0:
        performance_stock_text = performance_stock_text + f'  \n{stock}: :red[{performance_stock:.2%}]'
    else:
        performance_stock_text = performance_stock_text + f'  \n{stock}: {performance_stock:.2%}'

stock_portfolio_total_end = sum(stock_portfolio)
stock_portfolio_performance = stock_portfolio_total_end / stock_portfolio_total_start - 1
if stock_portfolio_performance > 0:
    stock_portfolio_performance_text =  f':green[{stock_portfolio_performance:.2%}]'
elif stock_portfolio_performance < 0:
    stock_portfolio_performance_text = f':red[{stock_portfolio_performance:.2%}]'
else:
    stock_portfolio_performance_text = f'{stock_portfolio_performance:.2%}'

st.write(f'''
# Performance prices of stocks
         
Performance:
{performance_stock_text}


Stock portfolio performance:
{stock_portfolio_performance_text}
         
''')

