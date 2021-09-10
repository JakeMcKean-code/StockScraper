
"""
Created on Sat Sep  4 12:25:25 2021

@author: Jake McKean
"""

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import datetime
 
# Function to convert a string to a float 
def str_to_num(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if(isinstance(df.iloc[0,df.columns.get_loc(column)], str)):
        df[column] = df[column].str.replace(',','')
        df[column] = df[column].astype(float)
    return df

# Function to group and split the full dataframe by the stock tickers
def split_dataframe(df: pd.DataFrame) -> list:
    list_of_dataframes: pd.DataFrame = []
    for code, df_code in df.groupby('stock_code'):
        list_of_dataframes.append(df_code)
    return list_of_dataframes

# Read in the dataframe and set the index and set the index to be a DatetimeIndex
df = pd.read_csv('StockData.csv', index_col = 'time',usecols = [0,2,3,4,5,6],names=['time','stock_code','price','change','percent change','volume'])
df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S')
df.index = pd.DatetimeIndex(df.index)

# split them up
list_of_dfs = split_dataframe(df)
for x in list_of_dfs:
    print(x)

# Get the latest data
latest_info = list_of_dfs[0].iloc[-1,:] # last row on all columns
latest_price = float(latest_info.iloc[1])
#latest_change = float(latest_info.iloc[2])
#latest_percent_change = float(latest_info.iloc[3].replace('%',''))

# Resample data to get the ohlc candlestick format
data = list_of_dfs[0]['price'].resample('1Min').ohlc()   
# Add new columns for rolling averages: !! NOTE add the drop rows code to get rid of NaNs that come from rolling averages
data['MA5'] = data['close'].rolling(1).mean()
data['MA10'] = data['close'].rolling(10).mean()
data['MA20'] = data['close'].rolling(20).mean()
# Make the index column a datetime format for the graph
data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')

# Create a counter the length of the data columns
candle_counter = range(len(data['open'])) # can use any column
ohlc = []
# Loop over the counter and add the ohlc data to the list
for candle in candle_counter:
    append_me = candle_counter[candle], data['open'][candle],\
        data['high'][candle], data['low'][candle], \
            data['close'][candle]
    ohlc.append(append_me) # This is a list of tuples, each tuple is the ohlc info for the row in the resample
    
# ------------------------------------------------------------------------------------------------------------
# Counter and x,y values for the graph
counter = count() # Just counts up one number at a time
x_vals = list() # empty list for the x and y vals
y_vals = list()

# Animation function
def animate(i):
    # count 1 up in the counter
    count = next(counter)
    # clear current axis
    plt.cla()
    # append timestamp to the x values and price to the y values
    x_vals.append(list_of_dfs[0].index[count])
    y_vals.append(list_of_dfs[0]['price'][count])
    # plot the graph
    plt.plot(x_vals,y_vals)
    #print(x_vals)
    #plt.xticks([])

# ani function that draws to gcf (get current figure), uses the animate function for its animation and updates at an interval of 1000ms
ani = FuncAnimation(plt.gcf(),animate, interval = 1000)
plt.show()