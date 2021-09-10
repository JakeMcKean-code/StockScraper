#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 12:25:25 2021

@author: jake
"""
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
import random
from matplotlib.animation import FuncAnimation
import datetime

def str_to_num(df, column):
    if(isinstance(df.iloc[0,df.columns.get_loc(column)], str)):
        df[column] = df[column].str.replace(',','')
        df[column] = df[column].astype(float)
    return df

def split_dataframe(df):
    list_of_dataframes = []
    for code, df_code in df.groupby('stock_code'):
        list_of_dataframes.append(df_code)
    return list_of_dataframes


df = pd.read_csv('StockData.csv', index_col = 'time',usecols = [0,2,3,4,5,6],names=['time','stock_code','price','change','percent change','volume'],skiprows=1)
df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S')
df.index = pd.DatetimeIndex(df.index)

print(df.index)
print(df)
df = str_to_num(df,'price')
listof = df.groupby(df['stock_code'] == 'ZM')
#for x in listof:
#    print(x) # returns 2 dataframes in a tuple with the True/False statement that relates to the boolean requirement

# Second way of grouping them
'''
df1, df2 = [x for y, x in df.groupby(df['stock_code'] == 'NFLX')] # hence we want to split them both here 
print(df1)
print('-----')
print(df2)
'''
# split them up
list_of_dfs = split_dataframe(df)
for x in list_of_dfs:
    print(x)


latest_info = list_of_dfs[0].iloc[-1,:] # last row on all columns
latest_price = float(latest_info.iloc[1])
#latest_change = float(latest_info.iloc[2])
#latest_percent_change = float(latest_info.iloc[3].replace('%',''))
#print(latest_price, latest_change, latest_percent_change)

data = list_of_dfs[0]['price'].resample('1Min').ohlc()   # Candlestick chart format


#data['time'] = pd.to_datetime(data['time'], format = "%Y-%m-%d %H:%M:%S") # triple check that it's a datetime format

data['MA5'] = data['close'].rolling(1).mean()
data['MA10'] = data['close'].rolling(10).mean()
data['MA20'] = data['close'].rolling(20).mean()
data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')

print(data)

candle_counter = range(len(data['open'])) # can use any column
ohlc = []
for candle in candle_counter:
    append_me = candle_counter[candle], data['open'][candle],\
        data['high'][candle], data['low'][candle], \
            data['close'][candle]
    ohlc.append(append_me)

print(candle_counter)
print(type(ohlc[0]))

counter = count() # Just counts up one number at a time
x_vals = list()
y_vals = list()


def animate(i):
    count = next(counter)
    plt.cla()
    time_stamp  = datetime.datetime.now() - datetime.timedelta(hours = 5)
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    x_vals.append(list_of_dfs[0].index[count])
    y_vals.append(list_of_dfs[0]['price'][count])
    plt.plot(x_vals,y_vals)
    #print(x_vals)
    #plt.xticks([])

ani = FuncAnimation(plt.gcf(),animate, interval = 1000)

plt.show()

#df.plot.scatter('time','price')

#df = (df['price'].resample('1Min')) # Candlestick chart format
#data['time'] = data.index
#data['time'] = pd.to_datetime(data['time'], format = "%Y-%m-%d %H:%M:%S")

#df2 = pd.DataFrame(df.ohlc())
#df2['MA5'] = df2['close'].rolling(5).mean()




#print((data.ohlc()['close'].rolling(5).mean()))
