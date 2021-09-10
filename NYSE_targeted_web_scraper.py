import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime

'''
def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div',{'class': class_path})   # find specific div using a class path
    try:
        spans = web_content_div[0].find_all('span')   # inside each div there are spans, find them all
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = [] # set to empty list if there is an index error for the spans in the divs
    return texts

# get functions to get the stock price from url
def real_time_stock(stock_code):
    url = 'https://ih.advfn.com/stock-market/NYSE/alcoa-' + stock_code + 'AA/stock-price' # generalise url so we can get any stock code
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text,'html.parser') # get request and parse it
        # we want to find the divs and then find the info inside the divs
        texts = web_content_div(web_content, 'price-info') # got class path from the website
        if texts != []:
              # if it's not empty then we set the price and the change accordingly
             price, change = texts[0], texts[1]
        else: 
              price, change = [], []
        # Do the same but now searching different class paths for diffrerent information on the site
        texts = web_content_div(web_content, 'TableElement')
        if texts!=[]:
            for count, vol in enumerate((texts)):
                if vol == "Volume":
                    print('here now for volsss --------------------')
                    volume = texts[count + 1]
                else:
                    volume = []
                    print('bad vols :(')

    except ConnectionError:
        price, change, volume, stock_code = [], [], [], [], [], []
    return price, change, volume, stock_code # now we have a lot more information about any stock

stocks = ['AA']

while(True):
    for stock_codes in stocks:
        col = [] # column
        timestamp = datetime.datetime.now() - datetime.timedelta(hours = 5) # take into account time difference between here and NY
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S') # give specific format to the date and time
        info = []
        col = [timestamp] # make a column with the timestamp
        stock_price, change, volume, stock_code = real_time_stock(stock_codes)
        info.append(stock_code) # add the stock code to the list
        info.extend([stock_price]) # extend the stock price and other info to make a 1D list of info
        info.extend([change])
        info.extend([volume])
        col.extend(info) # add the timestamp to the start of the row
        df = pd.DataFrame(col)
        df= df.T # transpose it so it is sideways (along the x)
        df.to_csv(str(timestamp[0:11]) + 'stock_data.csv', mode = 'a', header = False) # save to a csv file
        info.clear()
        col.clear()
        del(df)
    time.sleep(5)
'''

def get_data(code, company_name: list, company_ticker, company_stock, change, percent_change, volume):
    url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    page = requests.get(url)
    page_text: str = page.text
    soup = BeautifulSoup(page.text, 'html.parser')
    odd_rows: list = soup.find_all('tr', attrs={'class':'ts0'})
    even_rows: list = soup.find_all('tr', attrs={'class':'ts1'})

    row_td: list = [] 
    for element in odd_rows:
        row = element.find_all('td')
        row_td.append(row)
        if(row[1].text.strip() == code):
            company_name.append(row[0].text.strip()) 
            company_ticker.append(row[1].text.strip()) 
            company_stock.append(float(str(row[3].text.strip())))
            change.append(float(str(row[4].text.strip()))) 
            percent_change.append(float(str(row[5].text.strip()).replace('%',''))) 
            volume.append(float(str(row[6].text.strip()).replace(',','')))  

    for element in even_rows:
        row = element.find_all('td')
        row_td.append(element.find_all('td'))
        if(row[1].text.strip() == code):
            company_name.append(row[0].text.strip()) 
            company_ticker.append(row[1].text.strip()) 
            company_stock.append(float(row[3].text.strip()))
            change.append(float(str(row[4].text.strip()))) 
            percent_change.append(float(str(row[5].text.strip()).replace('%',''))) 
            volume.append(float(str(row[6].text.strip()).replace(',','')))   
        
    name = np.array(company_name)
    ticker = np.array(company_ticker)
    stock = np.array(company_stock)
    change = np.array(change)
    percent_change = np.array(percent_change)
    volume = np.array(volume)
  
    name = np.delete(name,0)
    ticker = np.delete(ticker,0)
    stock = np.delete(stock,0)
    
    name = name.reshape(len(name),1)
    ticker = ticker.reshape(len(ticker),1)
    stock = stock.reshape(len(stock),1)
    change = change.reshape(len(change),1)
    percent_change = percent_change.reshape(len(percent_change),1)
    volume = volume.reshape(len(volume),1)

    merged = np.concatenate((name,ticker,stock, change, percent_change, volume),axis=1)
    data = pd.DataFrame({"Company name":merged[:,0], "Company ticker":merged[:,1],"Stock Price":merged[:,2], "Change":merged[:,3], "Percent Change":merged[:,4], "Volume":merged[:,5]})
    print(data.head())
    return data

stocks = ['AA', 'ABEV']
while True:
    for code in stocks:
        timestamp = datetime.datetime.now() - datetime.timedelta(hours = 5) # take into account time difference between here and NY
        timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        company_name = [str]
        company_ticker = [str]
        company_stock = [float]
        change = []
        percentage_change = []
        volume = []
        df = get_data(code, company_name, company_ticker, company_stock, change, percentage_change, volume)
        df.to_csv(str(timestamp[0:11]) + 'stock_data.csv', mode = 'a', header = False, index=None)
        del(df)
        print('----------------')
    time.sleep(5)
