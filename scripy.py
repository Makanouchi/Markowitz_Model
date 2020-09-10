import yfinance as yf
from datetime import date
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt




#stock_list= ['WMT','AAPL']
msft = yf.Ticker("MSFT")

#mathematical functions
def getStockData(stock_list,date_today):
	data = yf.download(stock_list,str(date_today-timedelta(days=1095)),str(date.today()))['Adj Close']
	return data


def getReturns(data):
	daily_returns=((data-data.shift(1))/data.shift(1))
	daily_returns=daily_returns.iloc[1:]
	return daily_returns

def showReturns(daily_returns):
	plt.figure()
	daily_returns.plot()
	plt.show()

def expected_portfolio_returns(daily_returns,weights,len):
	x=np.sum(daily_returns.mean()*weights)
	return x

def stddev_returns(daily_returns,weights,len):
	weights=np.array(weights)
	x=np.sqrt(np.dot(weights.T,np.dot(daily_returns.cov(),weights)))
	return x

def generateRandomPortfolios(stocks,daily_returns):
	preturns=[]
	pvariance=[]
	sharp_ratio=0
	optimum_weights=[]
	max_return=0
	min_variance=0
	for i in range(10001):
		weights=np.random.random(len(stocks))
		weights/=np.sum(weights)
		curr_return=expected_portfolio_returns(daily_returns,weights,len(stocks))
		curr_variance=stddev_returns(daily_returns,weights,len(stocks))
		preturns.append(curr_return)
		pvariance.append(curr_variance)
		if((curr_return/curr_variance)>sharp_ratio):
			sharp_ratio=(curr_return/curr_variance)
			optimum_weights=weights
			max_return=curr_return
			min_variance=curr_variance
	preturns=np.array(preturns)
	pvariance=np.array(pvariance)
	return preturns,pvariance,optimum_weights



import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

#styling components
local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
html_temp = """
		<div style="background-color:#4F8BF9;padding:10px">
		<h1 style="color:{};text-align:center;">{}</h1>
		</div>
		"""
html_temp1 = """
		<div style="background-color:#4F8BF9;padding:10px">
		<h2 style="color:{};text-align:center;">{}</h2>
		</div>
		"""


st.markdown(html_temp.format("yellow","Markowitz Optimization"),unsafe_allow_html=True)

stocks=['AAPL', 'WMT', 'AMZN','GOOG','BA','MSFT','MMM','NKE','JNJ','MCD']
icon("search")
stock_list = st.multiselect('STOCKS TO ADD IN YOUR PORTFOLIO:',stocks)

#st.title("Daily returns of stocks in PortFolio")
st.markdown(html_temp1.format("yellow","Daily returns of Stocks"),unsafe_allow_html=True)
data=getStockData(stock_list,date.today())
daily_returns=getReturns(data)
if(len(daily_returns)>0):
	showReturns(daily_returns)
	st.pyplot()

st.markdown(html_temp1.format("yellow","Distribution of returns"),unsafe_allow_html=True)
daily_returns.hist(bins=100)
st.pyplot()




#st.markdown(html_temp1.format("yellow","Monte Carlo Simulation"),unsafe_allow_html=True)
#st.write('expected_portfolio_returns:',expected_portfolio_returns(daily_returns,[0.25,0.25,0.25,0.25]))
#st.write('variance:',stddev_returns(daily_returns,[0.25,0.25,0.25,0.25]))
#preturns,pvariance=generateRandomPortfolios(stock_list,daily_returns)
#plt.figure(figsize=(10,6))
#plt.scatter(pvariance,preturns,c=preturns/pvariance,marker='o')
#plt.grid(True)
#plt.xlabel('Expected volatality')
#plt.ylabel('Expected Return')
#plt.plot(min_variance,max_return,'X')
#plt.colorbar(label='Sharpe Ratio')
#st.pyplot()

#st.write('Optimal weights',optimum_weights)

date_1=date.today()-timedelta(days=730)

money=[]
#money.append(1000)

no_shares=np.zeros(len(stock_list))
dates_for_plot=[]
#st.write('Prev:',prev_weights)
for i in range(10):
	curr_date=date_1+timedelta(days=(30*i))
	dates_for_plot.append(curr_date)
	data=getStockData(stock_list,curr_date)
	daily_returns=getReturns(data)
	preturns,pvariance,optimum_weights=generateRandomPortfolios(stock_list,daily_returns)
	price = yf.download(stock_list,str(curr_date+timedelta(days=1)),str(curr_date+timedelta(days=1)))['Open']
	while(price.empty):
		curr_date=curr_date+timedelta(days=1)
		price = yf.download(stock_list,str(curr_date+timedelta(days=1)),str(curr_date+timedelta(days=1)))['Open']
	#st.write("Prices:",price)
	if(i==0):
		money.append(1000)
	else:
		x=0
		#st.write('No of shares',no_shares)
		for j in range(len(stock_list)):
			x=x+(no_shares[j]*price[stock_list[j]].iloc[0])
		money.append(x)
	curr_value=money[len(money)-1]
	#st.write("Curr val",curr_value)
	for j in range(len(stock_list)):
		money_for_share=curr_value*optimum_weights[j]
		no_shares[j]=money_for_share/price[stock_list[j]].iloc[0]


plt.figure(figsize=(10,6))
plt.plot(dates_for_plot,money,marker='o')
plt.grid(True)
plt.xlabel('Time')
plt.ylabel('Value of PortFolio')
st.pyplot()


	




