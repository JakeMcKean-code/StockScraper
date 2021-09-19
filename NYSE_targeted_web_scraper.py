from os import name
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time
import datetime


def check_exchange(exchange: str) -> bool:
    if exchange == "NASDAQ":
        print(f"Using {exchange}.")
        return True
    elif exchange == "NYSE":
        print(f"Using {exchange}.")
        return True
    elif exchange == "AMEX":
        print(f"Using {exchange}.")
        return True
    else:
        #raise ValueError("Code not found.")
        print('ValueError: Code not found.')
        return False

def get_stock_codes(page_info) -> None:
    print("Available stock codes are: ")
    list_of_codes = []
    for element in page_info:
        row = element.find_all('td')
        list_of_codes.append(row[1].text.strip())
    print(list_of_codes)
    return list_of_codes

def soup_parser(exchange) -> BeautifulSoup:
    if exchange == "NASDAQ":
        url: str = 'https://www.advfn.com/nasdaq/nasdaq.asp'
    elif exchange == "NYSE":
        url: str = 'https://www.advfn.com/nyse/newyorkstockexchange.asp'
    elif exchange == "AMEX":
        url: str = 'https://www.advfn.com/amex/americanstockexchange.asp'
    page = requests.get(url)
    page_text: str = page.text #line not needed at the moment
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def access_page_info(exchange) -> list:
    soup = soup_parser(exchange)
    info_rows: list = soup.find_all('tr', attrs={'class':['ts0', 'ts1']})
    return info_rows

def get_data(page_info, stock_code) -> list:
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


def create_csv(file_name: str, exchange, stock_list, interupt_time, interval_time) -> None:#interupt and interval time are passed as seconds
    
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
            df.to_csv(f'{file_name}.csv', mode='a', index=False, header=False)#saves all vales at once at the end of scraping
            del(df)

        time.sleep(interval_time)#adds a sleep to the scaper after scraping the desired companies
        current_time = time.time()


def run_scraping(file_name: str, run_time: int, sleep_time: int):
    stock_codes: list = []
    loop_condition: bool = False
    while loop_condition == False:
        exchange = input("Enter exchange (Allowed exchanges are: NASDAQ, NYSE, AMEX): ")
        if(check_exchange(exchange.upper()) == True):
            loop_condition = True
            page_info = access_page_info(exchange.upper())
            stock_codes = get_stock_codes(page_info)

    loop_condition = False
    while loop_condition == False:
        stocks = input("Enter your stock codes separated by a space: ").split()

        if len(stocks != 7):
            print('Error: Please enter 7 stock codes to track.')
            loop_condition = False
            break
        
        for element, stock in enumerate(stocks):
            if stock.upper() not in stock_codes:
                print(f'ValueError: Code "{stock.upper()}" not found.')
                loop_condition = False
                break
            else:
                loop_condition = True
                stocks[element] = stock.upper()
    print(f'Using stock codes: {stocks}.')

    create_csv(file_name, exchange, stocks, run_time, sleep_time)