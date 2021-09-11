from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime


def soup_parser():
    url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    page = requests.get(url)
    page_text: str = page.text
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def access_page_info():
    soup = soup_parser()
    info_rows: list = soup.find_all('tr', attrs={'class':['ts0', 'ts1']})
    return info_rows

def get_data(page_info, stock_code):
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


def scraping(stock_list, interupt_time, interval_time):#interupt and interval time are passed as seconds
    df = pd.DataFrame(columns=["Time", "Company name", "Company ticker", "Stock Price", "Change", "Percent Change", "Volume"])

    start_time = time.time()
    current_time = time.time()

    while current_time - start_time < interupt_time:
        page_info = access_page_info()#returns the page information
        time_stamp = datetime.datetime.now() - datetime.timedelta(hours=5)#creates a time stamp for when the page was accessed and converts UK time to NY time
        time_stamp = time_stamp.strftime('%y-%m-%d %H:%M:%S')#format the time stamp
        for stock_code in stock_list:
            information: list = [time_stamp]#information list created and time_stamp added into it
            information.extend(get_data(page_info, stock_code))#returns the stock information and adds it into the list of information
            df.loc[len(df)] = information#adds the information list to the datatframe
            df.to_csv('Test.csv',index=False)#saves all vales at once at the end of scraping

        time.sleep(interval_time)#adds a sleep to the scaper after scraping the desired companies
        current_time = time.time()

stocks = ['AA', 'ABEV']
scraping(stocks, 60, 5)


'''def get_data(code, company_name: list, company_ticker, company_stock, change, percent_change, volume, time_stamp):
    url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    page = requests.get(url)
    page_text: str = page.text
    soup = BeautifulSoup(page.text, 'html.parser')
    info_rows: list = soup.find_all('tr', attrs={'class':['ts0', 'ts1']})

    for element in info_rows:
        row = element.find_all('td')
        if(row[1].text.strip() == code):
            company_name.append(row[0].text.strip()) 
            company_ticker.append(row[1].text.strip()) 
            company_stock.append(float(str(row[3].text.strip())))
            change.append(float(str(row[4].text.strip()))) 
            percent_change.append(float(str(row[5].text.strip()).replace('%',''))) 
            volume.append(float(str(row[6].text.strip()).replace(',','')))  

    time = np.array([time_stamp])    
    name = np.array(company_name)
    ticker = np.array(company_ticker)
    stock = np.array(company_stock)
    change = np.array(change)
    percent_change = np.array(percent_change)
    volume = np.array(volume)
    
    print(name)
    name = np.delete(name,0)
    print(name)
    ticker = np.delete(ticker,0)
    stock = np.delete(stock,0)
    
    time = time.reshape(len(time),1)
    name = name.reshape(len(name),1)
    ticker = ticker.reshape(len(ticker),1)
    stock = stock.reshape(len(stock),1)
    change = change.reshape(len(change),1)
    percent_change = percent_change.reshape(len(percent_change),1)
    volume = volume.reshape(len(volume),1)

    merged = np.concatenate((time, name,ticker,stock, change, percent_change, volume),axis=1)
    data = pd.DataFrame({"Time": merged[:,0], "Company name":merged[:,1], "Company ticker":merged[:,2],"Stock Price":merged[:,3], "Change":merged[:,4], "Percent Change":merged[:,5], "Volume":merged[:,6]})
    #print(data.head())
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
        df = get_data(code, company_name, company_ticker, company_stock, change, percentage_change, volume, timestamp)
        #df.to_csv(str(timestamp[0:11]) + 'stock_data.csv', mode = 'a', header = False, index=None)
        del(df)
        print('----------------')
    time.sleep(5)'''
