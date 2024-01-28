#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:04:31 2024

@author: colegauerkemacbook
================================================
This is a program in python that will take in any stock symbol and download the desire data, and return with
a graph that compares the Risk (std on x axis) and the Returns (mean returns on y axis) over a desired time period

It implements the pandas library to make the data easy to interpret and create files, numpy to perform calculations,
matplotlib for the graphs, and yfinance which downloads the data from yahoo finance

This program was orignally written and executed in a Jupyter Lab Notebook, which I will also attach in the repository.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('ggplot')

#Downloading the desired data about the desired stocks using the 'yfinance' library frin the last 5 years, can do as many stocks as desired
#Sometimes yfinance is tricky and the data doesn't download, I have tried to diagnose the issue but it is very unpredictable,
#Restarting the Kernel and Clearing the variables usually helps
ticker = ['AMZN','CVX', 'GOOGL']
stocks = yf.download(ticker,start='2019-01-01',end='2024-01-01')

#Converting the stock data into a CSV file, making it easier to read/present
stocks.to_csv("stock_data.csv")
stocks = pd.read_csv("stock_data.csv",header=[0,1],index_col=[0],parse_dates=[0])

#Seperating the closing values from each stocks and dealing solely with the closing values
close_data = stocks.loc[:,"Close"].copy()

#Because these stocks all move at different volumes, I believe it is better to work with the percentages instead of the real values
#This normalizes the data into percentages and plots them
norm_close_data = close_data.div(close_data.iloc[0]*(100))
norm_close_data.plot(figsize=(15,12),fontsize=12)

#Gather the mean returns and standard deviation
returns = norm_close_data.pct_change().dropna()
summary = returns.describe().T.loc[:,['mean','std']]
summary["mean"]=summary["mean"]*252
summary["std"]=summary['std']*np.sqrt(252)

#Creates the Risk/Return Plot
summary.plot(kind="scatter",x="std",y="mean",figsize=(12,8),s=50,fontsize=15)
for i in summary.index:
    plt.annotate(i,xy=(summary.loc[i,"std"]+0.002,summary.loc[i,"mean"]+0.002),size=15)
plt.xlabel("Annual risk(std)",fontsize=15)
plt.ylabel("Annual return(mean)",fontsize=15)
plt.title('Risk Return', fontsize=25)

