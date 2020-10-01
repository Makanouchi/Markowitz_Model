import pandas_datareader as web
import numpy as np
from datetime import date
from datetime import timedelta
tickers=["AAPL","GOOG","RY","HPQ"]

# Get market cap (not really necessary for you)
market_cap_data =np.array(web.get_quote_yahoo(tickers,date.today()-timedelta(days=100),date.today()-timedelta(days=100))['marketCap'])

market_cap_data=market_cap_data/np.sum(market_cap_data)
print(market_cap_data)