# import streamlit as st
# import pandas as pd
# import yfinance as yf


# @st.cache_data
# def loading_data(ticker_list):
#     data_stock = yf.download(ticker_list, start='1900-01-01', period='1d')
#     return data_stock['Close']

# def loading_tickers():
#     tickers = pd.read_csv('IBOVDia_12-08-24.csv', sep=';').reset_index()
#     tickers = list(tickers['index'])
#     tickers = [ticker + '.SA' for ticker in tickers]
#     return tickers

# tickers_list = loading_tickers()

# datas = loading_data(tickers_list)

# st.write('''
# # App prices of stocks
# ''')

# st.sidebar.header('Filters')

# ticker_list = st.sidebar.multiselect('Choose your shares', datas.columns)
# if ticker_list:
#     datas = datas[ticker_list]
#     if len(ticker_list) == 1:
#         stock = ticker_list[0]
#         datas = datas.rename(columns={stock: 'Close'})

# start_date = datas.index.min().to_pydatetime()
# end_date = datas.index.max().to_pydatetime()
# interval_date = st.sidebar.slider('Filter a time interval', min_value=start_date, max_value=end_date, 
#                   value=(start_date, end_date))

# datas = datas.loc[interval_date[0]:interval_date[1]]

# st.line_chart(datas)

# performance_stock_text = ''

# if len(ticker_list)==0:
#     ticker_list = list(datas.columns)
# elif len(ticker_list)==1:
#     datas = datas.rename(columns={'Close': stock} )

# stock_portfolio = [1000 for stock in ticker_list]
# stock_portfolio_total_start = sum(stock_portfolio)

# for i, stock in enumerate(ticker_list):
#     performance_stock = float(datas[stock].iloc[-1] / datas[stock].iloc[0] - 1)

#     stock_portfolio[i] = stock_portfolio[i] * (1 + performance_stock)

#     if performance_stock > 0:
#         performance_stock_text = performance_stock_text + f'  \n{stock}: :green[{performance_stock:.2%}]'
#     elif performance_stock < 0:
#         performance_stock_text = performance_stock_text + f'  \n{stock}: :red[{performance_stock:.2%}]'
#     else:
#         performance_stock_text = performance_stock_text + f'  \n{stock}: {performance_stock:.2%}'

# stock_portfolio_total_end = sum(stock_portfolio)
# stock_portfolio_performance = stock_portfolio_total_end / stock_portfolio_total_start - 1
# if stock_portfolio_performance > 0:
#     stock_portfolio_performance_text =  f':green[{stock_portfolio_performance:.2%}]'
# elif stock_portfolio_performance < 0:
#     stock_portfolio_performance_text = f':red[{stock_portfolio_performance:.2%}]'
# else:
#     stock_portfolio_performance_text = f'{stock_portfolio_performance:.2%}'

# st.write(f'''
# # Performance prices of stocks
         
# Performance:
# {performance_stock_text}


# Stock portfolio performance:
# {stock_portfolio_performance_text}
         
# ''')

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime

# Cache para carregar dados de ações
@st.cache_data(ttl=3600)  # Cache com TTL para evitar dados muito antigos
def loading_data(ticker_list):
    data_stock = yf.download(ticker_list, start='1900-01-01', period='1d')
    return data_stock['Close']

# Cache para carregar os tickers do CSV
@st.cache_data
def loading_tickers():
    tickers = pd.read_csv('IBOVDia_12-08-24.csv', sep=';').reset_index()
    tickers = tickers['index'].tolist()
    tickers = [ticker + '.SA' for ticker in tickers]
    return tickers

# Carrega os tickers e os dados
tickers_list = loading_tickers()
datas = loading_data(tickers_list)

st.title('App Prices of Stocks')
st.sidebar.header('Filters')

# Filtragem dos tickers
selected_tickers = st.sidebar.multiselect('Choose your shares', datas.columns)
if selected_tickers:
    datas = datas[selected_tickers]

# Intervalo de datas
start_date = st.sidebar.date_input('Start date', value=datas.index.min().date(), min_value=datas.index.min().date(), max_value=datas.index.max().date())
end_date = st.sidebar.date_input('End date', value=datas.index.max().date(), min_value=datas.index.min().date(), max_value=datas.index.max().date())

# Filtro por intervalo de datas
datas = datas.loc[start_date:end_date]

# Exibição do gráfico
st.line_chart(datas)

# Cálculo de performance
performance_stock_text = ''
stock_portfolio = [1000] * len(selected_tickers)
stock_portfolio_total_start = sum(stock_portfolio)

if stock_portfolio_total_start == 0:
    st.write("O portfólio de ações está vazio ou houve um erro na seleção de ações.")
    st.stop()

for i, stock in enumerate(selected_tickers):
    performance_stock = (datas[stock].iloc[-1] / datas[stock].iloc[0]) - 1
    stock_portfolio[i] *= (1 + performance_stock)

    color = 'green' if performance_stock > 0 else 'red'
    performance_stock_text += f'  \n{stock}: :{color}[{performance_stock:.2%}]'

stock_portfolio_total_end = sum(stock_portfolio)
stock_portfolio_performance = (stock_portfolio_total_end / stock_portfolio_total_start) - 1

color = 'green' if stock_portfolio_performance > 0 else 'red'
stock_portfolio_performance_text = f':{color}[{stock_portfolio_performance:.2%}]'

# Exibição da performance
st.write(f'''
# Performance Prices of Stocks
         
Performance:
{performance_stock_text}

Stock portfolio performance:
{stock_portfolio_performance_text}
''')
