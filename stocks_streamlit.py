import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import fbprophet
import json



title="""
    <h1 style="text-align:center;"><font color='blue'>Stocks Analysis of some listed companies</h1></font>
    <h4 style="text-align:center;">"An investment in knowledge pays the best interest"   &nbsp;&nbsp;&nbsp;&nbsp; -Benjamin Franklin</h4>
    <br>
    """
    
st.markdown(title,unsafe_allow_html=True)


d=pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
df=['MICROSOFT','APPLE','GOOGLE']
df=sorted(df) 
company_symbol = st.sidebar.selectbox('Select your company',d)
import yfinance as yf
#dictonary={"APPLE":"AAPL","MICROSOFT":"MSFT","GOOGLE":"GOOGL"}
#company_symbol=(dictonary)[company]

try:
    data=yf.Ticker(company_symbol)
except KeyError:
    st.write("Details unavailable")
start=st.sidebar.date_input(label="start date",value=None,min_value=None,max_value=datetime.date.today(),key=None).strftime("%Y-%m-%d")
end=st.sidebar.date_input(label="end date",value=None,min_value=None,max_value=datetime.date.today(),key=None).strftime("%Y-%m-%d")
company_data=data.history(period='1d',start=start,end=end)
company_data.reset_index(inplace=True)
info=data.info

try:
    logo='<img src={} style="height:150px;width:150px;">'.format(info['logo_url'])
except KeyError:
    st.write("Details unavailable")
a,b,c = st.columns(3)
b.markdown(logo,unsafe_allow_html=True)
st.write("**All about {}**".format(info['longName']))
st.write(""" 
             
             
             
             """)
    
st.write(info['longBusinessSummary'])
st.write(""" 
             
             
             
             """)
st.write("**You can find more about us here:**"+"    "+" {}".format(info['website']))
    
    

    
    
    

st.write(""" 
             
             
             
             """)
title="""
    <h1 style="text-align:center;">Stocks history<h1>
    """
st.write(title,unsafe_allow_html=True)
st.write("**Stocks data of {} between {} and {}**".format(info['longName'],start,end))
st.write(company_data)                                       
st.write("**Stocks opening graphs of {} between {} and {}**".format(info['longName'],start,end))
fig = go.Figure()
st.line_chart(company_data.Open)
st.write(""" 
             
             
             
             """)
st.write("**Stocks high graphs of {} between {} and {}**".format(info['longName'],start,end))
st.line_chart(company_data.High)
st.write(""" 
             
             
             
             """)
st.write("**Stocks low graphs of {} between {} and {}**".format(info['longName'],start,end))
st.line_chart(company_data.Low)
st.write(""" 
             
             
             
             """)
st.write("**Stocks closing graphs of {} between {} and {}**".format(info['longName'],start,end))
st.line_chart(company_data.Close)
st.write(""" 
             
             
             
             """)
st.write("**Stocks volume graphs of {} between {} and {}**".format(info['longName'],start,end))
st.line_chart(company_data.Volume)

h1="""
<h1 style="text-align:center;">Predicting stocks of the future</h1>
"""
st.markdown(h1,unsafe_allow_html=True)
factor = st.selectbox('Select your stocks factor that has to be predicted' ,['Open','Close','Low','High','Volume'])
#getting dates for a specified period using fbprophet
def predict_dates(company_symbol,factor):
    start="2010-01-01"
    end=datetime.date.today()
    data=yf.download(company_symbol,start=start,end=end)
    data.reset_index(inplace=True)
    dates_data=data[['Date',factor]]
    dates_data=dates_data.rename(columns={"Date":"ds",factor:"y"})
    from fbprophet import Prophet
    prophet=Prophet()
    prophet.add_country_holidays(country_name='England')
    prophet.fit(dates_data)
    n=st.slider("Enter number of years to be predicted",1,15)
    period=365*n
    get_dates=prophet.make_future_dataframe(periods=period)
    get_data=prophet.predict(get_dates)
    st.write("**Predicted stocks in coming {} year(s)**".format(n))
    st.write(get_data.iloc[-period:])
    st.write("**Plotting predicted stocks in coming {} year(s)**".format(n))
    st.write(prophet.plot(get_data))
    st.write("**Yearly, Weekly and Daily trends of predicted values**")
    st.write(prophet.plot_components(get_data))
         
 
predict_dates(company_symbol,factor)
st.write(""" 
             
             
             
             """)
flag="""
    <h1 style="text-align:center;">Comparing any number of listed companies</h1>
    
    """
st.markdown(flag,unsafe_allow_html=True)             
companies=st.text_input("""
            
            Please enter atleast two companies to compare among themselves
            
            """)
companies=companies.upper()
if len(companies)!=0:
    
        
    data=yf.download(companies,start=start,end=end)
    data.reset_index(inplace=True)
    
    st.write(data)
def plotly_companies(factor,start,end,companies):
    import yfinance as yf
    import plotly.express as px
    import plotly.graph_objects as go
    if len(companies)!=0:
        fig = go.Figure()
        for i in companies.split(" "):
            data=yf.Ticker(i)
            company_data=data.history(period='1d',start=start,end=end)
            company_data.reset_index(inplace=True)
            
            fig.add_trace(go.Scatter(x=company_data["Date"], y=company_data[factor],
                    mode='lines',
                    name=i))
            fig.update_layout(margin=dict(l=50,r=100),width=700,height=600,title="<b>Time series graph for {} factor b/W {} and {}</b>".format(factor,start,end))
        st.plotly_chart(fig)
plotly_companies("Open",start,end,companies)
plotly_companies("Close",start,end,companies)        
plotly_companies("Low",start,end,companies)
plotly_companies("High",start,end,companies)
plotly_companies("Volume",start,end,companies)









