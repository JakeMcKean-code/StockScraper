from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime

class Scraper():
    def __init__(self) -> None:
        self.exchange_code: str
        self.stock_codes: list
        self.run_time: float = 10.0
        self.wait_time: float = 0.5

        self.User_Input()

    def access_page_info(self) -> list:
        if (self.exchange_code == "NASDAQ"):
            url: str = 'https://www.advfn.com/nasdaq/nasdaq.asp'
        elif (self.exchange_code == "NYSE"):
            url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
        elif (self.exchange_code == "AMEX"):
            url: str = 'https://www.advfn.com/amex/americanstockexchange.asp'
        page = requests.get(url)
        page_text: str = page.text 
        soup = BeautifulSoup(page_text, 'html.parser')
        info_rows: list = soup.find_all('tr', attrs={'class':['ts0', 'ts1']})
        return info_rows
    
    def get_stock_codes(self) -> list:
        page_info = self.access_page_info()
        print("Available stock codes are: ")
        list_of_codes = []
        for element in page_info:
            row = element.find_all('td')
            list_of_codes.append(row[1].text.strip())
        print(list_of_codes)
        return list_of_codes

    def check_exchange_code(self, exchange: str) -> bool:
        if exchange.upper() not in ["NASDAQ", "NYSE", "AMEX"]:
             print('ValueError: Code not found.')
             return False
        else:
            self.exchange_code = exchange.upper()
            return True
    
    def check_stock_codes(self, stock_codes: list, allowed_stock_codes: list) -> bool:
        if len(stock_codes) != 7:
                print('Error: Please enter 7 stock codes to track.')
                return False
            
        for stock in stock_codes:
            if stock.upper() not in allowed_stock_codes:
                print(f'ValueError: Code "{stock.upper()}" not found.')
                return False
            else:
                pass
        self.stock_codes = [stock.upper() for stock in stock_codes]
        return True

    
    def User_Input(self) -> None:
        loop_condition: bool = False
        while loop_condition == False:
            exchange = input("Enter exchange (Allowed exchanges are: NASDAQ, NYSE, AMEX): ")
            if(self.check_exchange_code(exchange.upper()) == True):
                loop_condition = True
                print(f'Using excahnge: {self.exchange_code}')
                allowed_stocks = self.get_stock_codes()

        loop_condition = False
        while loop_condition == False:
            stocks = input("Enter your stock codes separated by a space: ").split()
            if(self.check_stock_codes(stocks, allowed_stocks) == True):
                loop_condition = True
                print(f'Using stocks: {self.stock_codes}')

    def get_data(self, page_info, stock_code: str) -> list:
        for element in page_info:
            row = element.find_all('td')
            if(row[1].text.strip() == stock_code):
                company_name = row[0].text.strip()
                company_ticker = row[1].text.strip()
                company_stock = float(str(row[3].text.strip()))
                change = float(str(row[4].text.strip()))
                percent_change = float(str(row[5].text.strip()).replace('%',''))
                volume = float(str(row[6].text.strip()).replace(',',''))

                return  company_name, company_ticker, company_stock, change, percent_change, volume
        
    def update_csv(self, file_name: str) -> None:#interupt and interval time are passed as seconds
    
        start_time = time.time()
        current_time = time.time()

        while current_time - start_time < self.run_time:
            page_info = self.access_page_info()#returns the page information
            time_stamp = datetime.datetime.now().time()# - datetime.timedelta(hours=5)#creates a time stamp for when the page was accessed and converts UK time to NY time
            time_stamp = time_stamp.strftime('%H:%M:%S')#format the time stamp
            for stock_code in self.stock_codes:
                df = pd.DataFrame(columns=["Time", "Company name", "Company ticker", "Stock Price", "Change", "Percent Change", "Volume"])
                information: list = [time_stamp]#information list created and time_stamp added into it
                information.extend(self.get_data(page_info, stock_code))#returns the stock information and adds it into the list of information
                df.loc[len(df)] = information#adds the information list to the datatframe
                df.to_csv(f'{file_name}.csv', mode='a', index=False, header=False)#saves all vales at once at the end of scraping
                del(df)

            time.sleep(self.wait_time)#adds a sleep to the scaper after scraping the desired companies
            current_time = time.time()



"""
Created on Sat Sep  4 12:25:25 2021

@author: Jake McKean & Nathan Davies
"""
# Import scraing tool as a module

#from NYSE_targeted_web_scraper import run_scraping
#from test import Scraper

# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import axes
from itertools import count
from matplotlib.animation import FuncAnimation
import datetime
from pandas.core.frame import DataFrame
from matplotlib.gridspec import GridSpec
import mplfinance as mpf
from matplotlib.ticker import MaxNLocator

mc = mpf.make_marketcolors(up='#18b800',down='#ff3503',
                            wick={'up':'#18b800','down':'#ff3503'},
                        )
s  = mpf.make_mpf_style(marketcolors=mc)

# -------------------------------------- Create figure and subplots --------------------------------------
def graph_design(ax):
    ax.set_facecolor('#091217')
    ax.tick_params(axis="both", labelsize=6, colors='white')
    ax.ticklabel_format(useOffset=False)
    ax.spines['bottom'].set_color('#808080')
    ax.spines['top'].set_color('#808080')
    ax.spines['left'].set_color('#808080')
    ax.spines['right'].set_color('#808080')
    return ax

fig = plt.figure(figsize=(11,8))
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

ax_list = []
ax_list.append(graph_design(ax1))
ax_list.append(graph_design(ax1))
ax_list.append(graph_design(ax2))
ax_list.append(graph_design(ax3))
ax_list.append(graph_design(ax4))
ax_list.append(graph_design(ax5))
ax_list.append(graph_design(ax6))
ax_list.append(graph_design(ax7))
ax_list.append(graph_design(ax8))
ax_list.append(graph_design(ax9))


# -------------------------------------- Data functions --------------------------------------

def remove_NAN(df: pd.DataFrame):
    #Check if any nan values remain in the dataframe, if so delete the rows and reset the indiices
    if (df.isnull().sum().sum() != 0):
        df.dropna(inplace=True)


def preprocessing(CSV_filename: str) -> pd.DataFrame:
    # Read in the dataframe and set the index and set the index to be a DatetimeIndex
    df = pd.read_csv(f'{CSV_filename}.csv', index_col = 'time', usecols = [0,2,3,4,5,6], names=['time','stock_code','price','change','percent change','volume'])
    remove_NAN(df) #remove any rows with NAN values that may exist
    df.index = pd.to_datetime(df.index, format='%H:%M:%S')
    df.index = pd.DatetimeIndex(df.index)
    return df


def latest_values(df: pd.DataFrame) -> list:
    # Get the latest data
    latest_info = df.iloc[-1,:] # last row on all columns
    latest_price = float(latest_info.iloc[1])
    latest_change = float(latest_info.iloc[2])
    latest_percent_change = float(str(latest_info.iloc[3]).replace('%',''))
    return latest_price, latest_change, latest_percent_change


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
        if (elem == 0):#sets the first change to 0 since no previous close values exist
            changes.append(0)
        else:
            changes.append( round(current_close_val - previous_close_val, 2) )
    return changes


def resample(df: pd.DataFrame) -> pd.DataFrame:
    # Resample data to get the ohlc candlestick format
    data = df['price'].resample('10s').ohlc()
    data['volume'] = df['volume'].resample('10s').mean() #adds the mean of the resampled volume values to the resampled dataframe
    remove_NAN(data)#removes NAN rows produced by rolling averages
    data['change'] = calculate_change_in_close(data['close']) #adds the mean of the resampled price change values to the resampled dataframe
    
    # Make the index column a datetime format for the graph
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d %H:%M:%S')
    return data

# -------------------------------------- Plotting functions --------------------------------------
# Function to specify the plotting of ax1
def ax1_plotting(count: count, dataframe: pd.DataFrame, stock_code: str) -> None:
    # clear current axis
    ax1.cla()
    # Makes the plots
    df = dataframe.drop(columns=['change'])[:count+1]
    mpf.plot(df, type='candle',  ax=ax1, style=s, xrotation=0)
    mpf.plot(df, type='line', ax=ax1, volume = ax8, xrotation=0, style='charles')
    ax1.yaxis.set_ticks_position('left')
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.label.set_color('white')
    del df
   

    # Get the latest price and latest change for that specific stock
    latest_price = dataframe['close'][count]
    latest_change = dataframe['change'][count]

    # Adds the stock code and the current price above the main plot in black font with a yellow background
    ax1.text(0.005,1.10, f'{stock_code}: {latest_price}', transform=ax1.transAxes, color = 'black', fontsize = 18,
             fontweight = 'bold', horizontalalignment='left',verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))

    # Specifies the colour of the latest_change font depending on the value
    if str(latest_change)[0] == "-":
        colorcode = 'red'
    else:
        colorcode = '#18b800'

    # Adds the latest change (from close) above the main plot in red for -ve change and green for +ve change
    ax1.text(0.8,1.10, f'AAPL Latest Change: {latest_change}', transform=ax1.transAxes, color = colorcode, fontsize = 10,
             fontweight = 'bold', horizontalalignment='center',verticalalignment='center')

    # Get a timestamp
    time_stamp  = datetime.datetime.now()
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")

    # Adds the time stamp in the top right hand corner of the figure
    ax1.text(1.4,1.05,time_stamp,transform=ax1.transAxes, color = 'white', fontsize = 15,
             fontweight = 'bold', horizontalalignment='center',verticalalignment='center')

    # Adds a grid to the main plot
    ax1.grid(True, color = 'grey', linestyle = '-', which = 'major', axis = 'both',
             linewidth = 0.3)
    
# Function to specify the ax9 plotting
def ax9_plotting(count: count, dataframe: pd.DataFrame, stock_code: str) -> None:
    ax9.cla()
    # "Queue" system for only showing 10 points at a time
    if (count<10):
        df = dataframe.drop(columns=['change'])[:count+1]
        mpf.plot(df, type='candle',  ax=ax9, style=s, xrotation=0)
        mpf.plot(df, type='line', ax=ax9, xrotation=0, style='charles')
        ax9.yaxis.set_ticks_position('left')
        ax9.yaxis.set_label_position('left')
        ax9.yaxis.label.set_color('white')
        del df
    else:
        df = dataframe.drop(columns=['change'])[count-10:count+1]
        mpf.plot(df, type='candle',  ax=ax9, style=s, xrotation=0)
        mpf.plot(df, type='line', ax=ax9, xrotation=0, style='charles')
        ax9.yaxis.set_ticks_position('left')
        ax9.yaxis.set_label_position('left')
        ax9.yaxis.label.set_color('white')
        del df
    ax9.text(0.005,-0.8, f'{stock_code}: Recent history', transform=ax9.transAxes, color = 'black', fontsize = 13,
             fontweight = 'bold', horizontalalignment='left',verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    
    ax9.grid(True, color = 'grey', linestyle = '-', which = 'major', axis = 'both',
             linewidth = 0.3)

# Function to specify the plotting of the side panel plots
def side_panel_plotting(count: count, dataframe: pd.DataFrame, stock_code: str, axis) -> None:
    # Clear current axis
    axis.cla()
    # "Queue" system for only showing 10 points at a time
    if (count<10):
        df = dataframe.drop(columns=['change', 'volume'])[:count+1]
        mpf.plot(df, type='candle',  ax=axis, style=s, xrotation=0)
        mpf.plot(df, type='line', ax=axis, xrotation=0)
        axis.yaxis.set_ticks_position('right')
        axis.yaxis.set_label_position('right')
        axis.yaxis.label.set_color('white')
        del df
    else:
        df = dataframe.drop(columns=['change', 'volume'])[count-10:count+1]
        mpf.plot(df, type='candle',  ax=axis, style=s, xrotation=0)
        mpf.plot(df, type='line', ax=axis, xrotation=0)
        axis.yaxis.set_ticks_position('right')
        axis.yaxis.set_label_position('right')
        axis.yaxis.label.set_color('white')
        del df
    
    # Text for the side panel plots
    axis.text(1.3,0.8, f'{stock_code}', transform=axis.transAxes, color = 'black', fontsize = 12,
             fontweight = 'bold', horizontalalignment='left',verticalalignment='center',
             bbox=dict(facecolor='#FFBF00'))
    axis.grid(True, color = 'grey', linestyle = '-', which = 'major', axis = 'both',
             linewidth = 0.3)

# Function to control the aesthetics of the ax8 volume plot
def ax8_plotting():
    ax8.yaxis.label.set_color('white')
    ax8.ticklabel_format(axis='y',style='scientific')

# -------------------------------------- Animation functions --------------------------------------
# Animation function
def animate_live(i):
    for axis in ax_list:
        axis.xaxis.set_major_locator(MaxNLocator(3)) #produced Nbins and therefore Nbins+1 ticks

    # Count 1 up in the counter
    count = next(counter)
    file_name: str = '30-09-21'
    scraper.update_csv(file_name)
    df = preprocessing(file_name)
    # Split into each stock code
    list_of_codes, list_of_dfs = split_dataframe_by_stockcode(df)
    ax1_plotting(count, resample(list_of_dfs[0]), list_of_codes[0])
    ax9_plotting(count, resample(list_of_dfs[0]), list_of_codes[0])
    ax8_plotting()
    for i in range(1,len(list_of_dfs)):
        side_panel_plotting(count, resample(list_of_dfs[i]), list_of_codes[i], ax_list[i+1])

# -------------------------------------- Main --------------------------------------
if __name__ == '__main__':
    scraper = Scraper()
    # Counter values for the graph
    counter = count() # Just counts up one number at a time

    # ani function that draws to gcf (get current figure), uses the animate function for its animation and updates at an interval of 1000ms
    ani = FuncAnimation(fig, animate_live, interval = 500)
    
    # Defines padding between and around graphs
    plt.tight_layout(pad=10, w_pad=0.1, h_pad=0.1)
    plt.show()