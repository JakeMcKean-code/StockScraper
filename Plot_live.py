
"""
Created on Sat Sep  4 12:25:25 2021

@author: Jake McKean
"""
# Import scraing tool as a module
from matplotlib import axes
from NYSE_targeted_web_scraper import run_scraping

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import count
from matplotlib.animation import FuncAnimation
import datetime
from pandas.core.frame import DataFrame
from matplotlib.gridspec import GridSpec
#from mplfinance.original_flavor import candlestick_ochl
import mplfinance as mpf

mc = mpf.make_marketcolors(up='#18b800',down='#ff3503',
                            wick={'up':'#18b800','down':'#ff3503'},
                        )
s  = mpf.make_mpf_style(marketcolors=mc)

# -------------- Create figure and subplots ---------------------
def graph_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis="both", labelsize=8, colors='white')
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')
    return ax

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
    df = pd.read_csv('Test.csv', index_col = 'time', usecols = [0,2,3,4,5,6], names=['time','stock_code','price','change','percent change','volume'])
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
    list_of_codes: list = []
    for code, df_code in df.groupby('stock_code'):
        list_of_codes.append(code)
        list_of_dataframes.append(df_code)
    return list_of_codes, list_of_dataframes


def calculate_change_in_close(closes: list) -> list:
    #changes = np.arange(0, len(closes), 1)
    changes = []
    for elem, current_close_val in enumerate(closes):
        previous_close_val = closes[elem-1]
        if elem == 0:#sets the first change to 0 since no previous close values exist
            changes.append(0)
        else:
            changes.append( round(current_close_val - previous_close_val, 2) )
    return changes


def resample(df: pd.DataFrame) -> pd.DataFrame:
    # Resample data to get the ohlc candlestick format
    data = df['price'].resample('1Min').ohlc()
    data['volume'] = df['volume'].resample('1Min').mean() #adds the mean of the resampled volume values to the resampled dataframe
    remove_NAN(data)#removes NAN rows produced by rolling averages
    data['change'] = calculate_change_in_close(data['close']) #adds the mean of the resampled price change values to the resampled dataframe


    
    # Make the index column a datetime format for the graph
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    return data


def ax1_plotting(count: count, dataframe: pd.DataFrame, stock_code: str) -> None:
    # clear current axis
    ax1.cla()
    
    df = dataframe.drop(columns=['change'])[:count+1]
    mpf.plot(df, type='candle',  ax=ax1, style=s, xrotation=0)
    mpf.plot(df, type='line', ax=ax1, volume = ax8, xrotation=0, style='charles')#currently no way to add a legend that I can see
    ax1.yaxis.set_ticks_position('left')
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.label.set_color('white')
    del df


    latest_price = dataframe['close'][count]
    latest_change = dataframe['change'][count]
    #adds the stock code and the current price above the main plot in black font with a yellow background
    ax1.text(0.005,1.10, f'{stock_code}: {latest_price}', transform=ax1.transAxes, color = 'black', fontsize = 18,
             fontweight = 'bold', horizontalalignment='left',verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    if str(latest_change)[0] == "-":
        colorcode = 'red'
    else:
        colorcode = '#18b800'
    #adds the latest change (from open) above the main plot in red for -ve change and green for +ve change
    ax1.text(0.8,1.10, latest_change, transform=ax1.transAxes, color = colorcode, fontsize = 18,
             fontweight = 'bold', horizontalalignment='center',verticalalignment='center')
    time_stamp  = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    #adds the time stamp in the top right hand corner of the figure
    ax1.text(1.4,1.05,time_stamp,transform=ax1.transAxes, color = 'white', fontsize = 12,
             fontweight = 'bold', horizontalalignment='center',verticalalignment='center')
    #adds a grid to the main plot
    ax1.grid(True, color = 'grey', linestyle = '-', which = 'major', axis = 'both',
             linewidth = 0.3)
    '''legend = ax1.legend(loc='upper left', facecolor = '#121416', fontsize = 10) '''
    '''plt.setp(legend.get_texts(), color='w')'''


def side_panel_plotting(count: count, dataframe: pd.DataFrame, stock_code: str, axis) -> None:
    # clear current axis
    axis.cla()
    
    df = dataframe.drop(columns=['change', 'volume'])[:count+1]
    mpf.plot(df, type='candle',  ax=axis, style=s, xrotation=0)
    mpf.plot(df, type='line', ax=axis, xrotation=0)#currently no way to add a legend that I can see
    axis.yaxis.set_ticks_position('left')
    axis.yaxis.set_label_position('left')
    axis.yaxis.label.set_color('white')
    del df
    
    axis.text(1.02,0.5, f'{stock_code}', transform=axis.transAxes, color = 'black', fontsize = 18,
             fontweight = 'bold', horizontalalignment='left',verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    axis.grid(True, color = 'grey', linestyle = '-', which = 'major', axis = 'both',
             linewidth = 0.3)
    


def ax8_plotting():
    ax8.yaxis.label.set_color('white')
    ax8.ticklabel_format(axis='y',style='scientific')

# Animation function
def animate_live(i):
    df = preprocessing()

    #split into each stock code
    list_of_codes, list_of_dfs = split_dataframe_by_stockcode(df)

    # count 1 up in the counter
    count = next(counter)
    
    ax1_plotting(count, resample(list_of_dfs[0]), list_of_codes[0])
    ax8_plotting()

    side_panel_plotting(count, resample(list_of_dfs[1]), list_of_codes[1], ax2)
    side_panel_plotting(count, resample(list_of_dfs[2]), list_of_codes[2], ax3)
    #side_panel_plotting(count, resample(list_of_dfs[3]), list_of_codes[3], ax4)
    #side_panel_plotting(count, resample(list_of_dfs[4]), list_of_codes[4], ax5)
    #side_panel_plotting(count, resample(list_of_dfs[5]), list_of_codes[5], ax6)
    #side_panel_plotting(count, resample(list_of_dfs[6]), list_of_codes[6], ax7)

# -------------- Main ---------------------
if __name__ == '__main__':
    #run_scraping('InputTest', 60, 5) #runs the scraper and therefore makes the csv file    

    # ------------------------------------------------------------------------------------------------------------
    # Counter and x,y values for the graph
    counter = count() # Just counts up one number at a time

    # ani function that draws to gcf (get current figure), uses the animate function for its animation and updates at an interval of 1000ms
    ani = FuncAnimation(fig, animate_live, interval = 1000)
    
    #manager = plt.get_current_fig_manager()
    #manager.full_screen_toggle()
    plt.tight_layout(pad=4, w_pad=0.1, h_pad=0.1)
    plt.show()