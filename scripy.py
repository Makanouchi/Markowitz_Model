import yfinance as yf
from datetime import date
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import SessionState
from img_map import *
from PIL import Image
image = Image.open('img/icon-image.jpg')
import os


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


def img_to_bytes(img_path):
    img_bytes = os.path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


import streamlit as st

#add defaults settings
st.beta_set_page_config(
    page_title="Portfolio Optimization App",
    page_icon=image,
	layout="wide",
    initial_sidebar_state="expanded",
)


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
		<div style="background-color:black;padding:10px">
		<i><b><u><h1 style="color:{};text-align:center;">{}</h1></u></b></i>
		</div>
		"""
html_temp1 = """
		<div style="background-color:black;padding:10px">
		<h2 style="color:{};text-align:center;">{}</h2>
		</div>
		"""

#side bar code
html_sidebar = """
  <style>
    .reportview-container {
      flex-direction: row-reverse;
    }

    header > .toolbar {
      flex-direction: row-reverse;
      left: 1rem;
      right: auto;
    }

    .sidebar .sidebar-collapse-control,
    .sidebar.--collapsed .sidebar-collapse-control {
      left: auto;
      right: 0.5rem;
    }

    .sidebar .sidebar-content {
      transition: margin-right .3s, box-shadow .3s;
    }

    .sidebar.--collapsed .sidebar-content {
      margin-left: auto;
      margin-right: -21rem;
    }

    @media (max-width: 991.98px) {
      .sidebar .sidebar-content {
        margin-left: auto;
      }
    }
  </style>
"""

PAGES = [
    "Stock selection",
    "Stock Trends",
    "Daily Returns of Stock",
    "Distribution of Returns",
    "Portfolio Value"
]
st.markdown(html_sidebar, unsafe_allow_html=True)

st.sidebar.title("Navigation:")
selection = st.sidebar.radio("Go to", options=PAGES)


#stocks list
stocks=['AAPL', 'WMT', 'AMZN','GOOG','BA','MSFT','MMM','NKE','JNJ','MCD']

#page selection
session_state = SessionState.get(stock_list=[])
if(selection=="Stock selection"):
	st.markdown(html_temp.format("yellow","Stock Selection for Portfolio"),unsafe_allow_html=True)
	st.markdown(html_temp1.format("yellow","STOCKS TO ADD IN YOUR PORTFOLIO:"),unsafe_allow_html=True)
	icon("search")
	session_state.stock_list = st.multiselect('',stocks)
	img_list=[]
	for i in session_state.stock_list:
		image = Image.open(map_for_images[i]).convert("RGB")
		image=image.resize((100,100))
		img_list.append(image)
	st.image(img_list)
		
if(selection=="Stock Trends"):
	st.markdown(html_temp.format("yellow","Trends for Selected Stocks"),unsafe_allow_html=True)
	data=getStockData(session_state.stock_list,date.today())
	plt.figure(figsize=(10,6))
	plt.plot(data)
	plt.legend(session_state.stock_list)
	st.pyplot()
if(selection=="Daily Returns of Stock"):
	st.markdown(html_temp.format("yellow","Daily returns of Stocks"),unsafe_allow_html=True)
	data=getStockData(session_state.stock_list,date.today())
	daily_returns=getReturns(data)
	plt.figure(figsize=(10,6))
	plt.plot(daily_returns)
	plt.legend(session_state.stock_list)
	st.pyplot()
if(selection=="Distribution of Returns"):
	st.markdown(html_temp.format("yellow","Distribution of Stocks"),unsafe_allow_html=True)
	data=getStockData(session_state.stock_list,date.today())
	daily_returns=getReturns(data)
	daily_returns.hist(bins=100)
	st.pyplot()	







if(selection=="Portfolio Value"):
	st.markdown(html_temp.format("yellow","Portfolio Value"),unsafe_allow_html=True)
	with st.spinner('Loading Portfolio value...'):
		date_1=date.today()-timedelta(days=730)
		money=[]
		no_shares=np.zeros(len(session_state.stock_list))
		dates_for_plot=[]

		for i in range(10):
			curr_date=date_1+timedelta(days=(30*i))
			dates_for_plot.append(curr_date)
			data=getStockData(session_state.stock_list,curr_date)
			daily_returns=getReturns(data)
			preturns,pvariance,optimum_weights=generateRandomPortfolios(session_state.stock_list,daily_returns)
			price = yf.download(session_state.stock_list,str(curr_date+timedelta(days=1)),str(curr_date+timedelta(days=1)))['Open']
			while(price.empty):
				curr_date=curr_date+timedelta(days=1)
				price = yf.download(session_state.stock_list,str(curr_date+timedelta(days=1)),str(curr_date+timedelta(days=1)))['Open']
			#st.write("Prices:",price)
			if(i==0):
				money.append(1000)
			else:
				x=0
				#st.write('No of shares',no_shares)
				for j in range(len(session_state.stock_list)):
					x=x+(no_shares[j]*price[session_state.stock_list[j]].iloc[0])
				money.append(x)
			curr_value=money[len(money)-1]
			#st.write("Curr val",curr_value)
			for j in range(len(session_state.stock_list)):
				money_for_share=curr_value*optimum_weights[j]
				no_shares[j]=money_for_share/price[session_state.stock_list[j]].iloc[0]


	plt.figure(figsize=(10,6))
	plt.plot(dates_for_plot,money,marker='o')
	plt.grid(True)
	plt.xlabel('Time')
	plt.ylabel('Value of PortFolio')
	st.pyplot()
	st.success("Plot generated Successfully")


	




