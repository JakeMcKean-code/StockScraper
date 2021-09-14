
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
from pandas.core.frame import DataFrame
from matplotlib.gridspec import GridSpec

# -------------- Create figure and subplots ---------------------

fig = plt.figure()
fig.patch.set_facecolor('#121416')
gs = fig.add_gridspec(6,6)
ax1 = fig.add_subplot(gs[0:4,0:4])
ax2 = fig.add_subplot(gs[0,4:6])
ax3 = fig.add_subplot(gs[1,4:6])
ax4 = fig.add_subplot(gs[2,4:6])
ax5 = fig.add_subplot(gs[3,4:6])
ax6 = fig.add_subplot(gs[4,4:6])
ax7 = fig.add_subplot(gs[5,4:6])
ax8 = fig.add_subplot(gs[4,0:4])
ax9 = fig.add_subplot(gs[5,0:4])

def graph_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis="both", labelsize=8, colors='white')
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')
    return ax

ax1 = graph_design(ax1)
ax2 = graph_design(ax2)
ax3 = graph_design(ax3)
ax4 = graph_design(ax4)
ax5 = graph_design(ax5)
ax6 = graph_design(ax6)
ax7 = graph_design(ax7)
ax8 = graph_design(ax8)
ax9 = graph_design(ax9)


# -------------- Data functions ---------------------

def remove_NAN(df: pd.DataFrame):
    #Check if any nan values remain in the dataframe, if so delete the rows and reset the indiices
    if df.isnull().sum().sum() != 0:
        df.dropna(inplace=True)


def preprocessing() -> pd.DataFrame:
    # Read in the dataframe and set the index and set the index to be a DatetimeIndex
    df = pd.read_csv('Test.csv', index_col = 'time',usecols = [0,2,3,4,5,6],names=['time','stock_code','price','change','percent change','volume'])
    remove_NAN(df) #remove any rows with NAN values that may exist
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S') # NOTE: Don't actually need this line 
    df.index = pd.DatetimeIndex(df.index)
    return df


def latest_values(df: pd.DataFrame) -> list:
    # Get the latest data
    latest_info = df.iloc[-1,:] # last row on all columns
    latest_price = float(latest_info.iloc[1])
    latest_change = float(latest_info.iloc[2])
    latest_percent_change = float(str(latest_info.iloc[3]).replace('%',''))
    return latest_price, latest_change, latest_percent_change


# Function to convert a string to a float 
def str_to_num(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if(isinstance(df.iloc[0,df.columns.get_loc(column)], str)):
        df[column] = df[column].str.replace(',','')
        df[column] = df[column].astype(float)
    return df


# Function to group and split the full dataframe by the stock tickers
def split_dataframe_by_stockcode(df: pd.DataFrame) -> list:
    list_of_dataframes: pd.DataFrame = []
    for code, df_code in df.groupby('stock_code'):
        list_of_dataframes.append(df_code)
    return list_of_dataframes


def resample_and_rolling(df: pd.DataFrame) -> pd.DataFrame:
    # Resample data to get the ohlc candlestick format
    data = df['price'].resample('1Min').ohlc()  
    # Add new columns for rolling averages: !! NOTE add the drop rows code to get rid of NaNs that come from rolling averages
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA10'] = data['close'].rolling(10).mean()
    data['MA20'] = data['close'].rolling(20).mean()

    remove_NAN(data)#removes NAN rows produced by rolling averages
    
    # Make the index column a datetime format for the graph
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    return data


def candle_ohlc(data: pd.DataFrame) -> list:
    # Create a counter the length of the data columns
    candle_counter = range(len(data['open'])) # can use any column
    ohlc = []
    # Loop over the counter and add the ohlc data to the list
    for candle in candle_counter:
        append_me = candle_counter[candle], data['open'][candle],\
            data['high'][candle], data['low'][candle], \
                data['close'][candle]
        ohlc.append(append_me) # This is a list of tuples, each tuple is the ohlc info for the row in the resample
    return ohlc

# Animation function
def animate(i):
    # count 1 up in the counter
    count = next(counter)
    # clear current axis
    ax1.cla()
    # append timestamp to the x values and price to the y values
    x_vals.append(list_of_dfs[0].index[count])
    y_vals.append(list_of_dfs[0]['price'][count])
    # plot the graph
    ax1.plot(x_vals,y_vals)
    #print(x_vals)
    #plt.xticks([])


# -------------- Main ---------------------
if(__name__ == '__main__'):
    df = preprocessing()

    #split into each stock code
    list_of_dfs = split_dataframe_by_stockcode(df)

    list_of_latest_values: list = []
    list_of_candle_ohlc: list = []

    for dataframe in list_of_dfs:
        list_of_latest_values.append(latest_values(dataframe))
        list_of_candle_ohlc.append( candle_ohlc( resample_and_rolling(dataframe) ) )

    # ------------------------------------------------------------------------------------------------------------
    # Counter and x,y values for the graph
    counter = count() # Just counts up one number at a time
    x_vals = list() # empty list for the x and y vals
    y_vals = list()

    # ani function that draws to gcf (get current figure), uses the animate function for its animation and updates at an interval of 1000ms
    ani = FuncAnimation(fig, animate, interval = 1000)

    #manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()

    plt.show()