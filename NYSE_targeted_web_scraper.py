from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime


def Get_exchange(exchange: str):
    if exchange == "NASDAQ":
        print("Using NASDAQ")
        return True
    elif exchange == "NYSE":
        print("Using NYSE")
        return True
    elif exchange == "AMEX":
        print("Using AMEX")
        return True
    else:
        raise ValueError("Code not found")

def get_stock_codes(page_info):
    print("Available stock codes are: ")
    list_of_codes = []
    for element in page_info:
        row = element.find_all('td')
        list_of_codes.append(row[1].text.strip())
    print(list_of_codes)

def soup_parser(exchange):
    if exchange == "NASDAQ":
        url: str = 'https://www.advfn.com/nasdaq/nasdaq.asp'
    elif exchange == "NYSE":
        url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    elif exchange == "AMEX":
        url: str = 'https://www.advfn.com/amex/americanstockexchange.asp'
    page = requests.get(url)
    page_text: str = page.text
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def access_page_info(exchange):
    soup = soup_parser(exchange)
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


def scraping(exchange, stock_list, interupt_time, interval_time):#interupt and interval time are passed as seconds
    
    start_time = time.time()
    current_time = time.time()

    while current_time - start_time < interupt_time:
        page_info = access_page_info(exchange)#returns the page information
        time_stamp = datetime.datetime.now() - datetime.timedelta(hours=5)#creates a time stamp for when the page was accessed and converts UK time to NY time
        time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')#format the time stamp
        for stock_code in stock_list:
            df = pd.DataFrame(columns=["Time", "Company name", "Company ticker", "Stock Price", "Change", "Percent Change", "Volume"])
            information: list = [time_stamp]#information list created and time_stamp added into it
            information.extend(get_data(page_info, stock_code))#returns the stock information and adds it into the list of information
            df.loc[len(df)] = information#adds the information list to the datatframe
            df.to_csv('inputTest.csv',mode='a',index=False, header=False)#saves all vales at once at the end of scraping
            del(df)

        time.sleep(interval_time)#adds a sleep to the scaper after scraping the desired companies
        current_time = time.time()

# --------------- Main ----------------

if __name__ == "__main__":
    exchange = input("Enter exchange: ")
    if(Get_exchange(exchange) == True):
        page_info = access_page_info(exchange)
        get_stock_codes(page_info)

    stocks = input("Enter your stock codes separated by a space: ")
    stocks = stocks.split()

    #stocks = ['AA','BABA','F','LYG','NOK']
    scraping(exchange, stocks, 60, 5)
