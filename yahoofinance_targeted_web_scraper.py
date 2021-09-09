'''
#Dependencies
'''


import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import numpy as np
import time



'''
#Functions to gather stock information
'''


def web_content_div(soup, class_path):
  find_all_div = soup.find_all('div', {'class': class_path})#similar to finding tr
  #This searches through all the div elements for the specific acompanying class_path attribute
  try:
    spans = find_all_div[0].find_all('span')#similar to finding td, the list brackets are a formality as there is only one element in the list anyway.
    #Once the specific div has been found, all span elements within that div (even if they are found within further nested divs) will be extracted
    texts = [span.get_text() for span in spans]#list of information from web page, for the example of the price and change, price is on the first span and change is the second span
  
  except IndexError as e:
    print(e)
    texts = []

  return texts

def price_scraper(soup):
  texts = web_content_div(soup, 'My(6px) Pos(r) smartphone_Mt(6px)')#This extracts the price and change in price
  if texts != []:
    price, change = texts[0], texts[1]
  else:
    price, change = [], []
  return price, change

def volume_scraper(soup):
  left_texts = web_content_div(soup, 'D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b) smartphone_W(100%) smartphone_Pend(0px) smartphone_BdY smartphone_Bdc($seperatorColor)')#Class path of the table of information
  #right_texts = web_content_div(web_content, 'D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a) smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)')#Class path of the table of information
  #texts = left_texts + right_texts
  no_volume: bool = True
  if left_texts != []:
    for count, elem in enumerate(left_texts):
      if elem == 'Volume':#looks through the generated list for the volume key word
        no_volume = False
        return left_texts[count+1]#if volume key word is found then the associated value is returned

  if no_volume == True:#if volume key word is not found then a null value is returned
    return []
      

def real_time_price(stock_code):
  url: str = 'https://finance.yahoo.com/quote/'+stock_code+'?p='+stock_code+'&.tsrc=fin-srch'
  try: 
    page = requests.get(url)
    web_content = BeautifulSoup(page.text, 'html.parser')#soup
    
    price, change = price_scraper(web_content)
    volume = volume_scraper(web_content)
    #del page
    #del web_content

  except ConnectionError as e:
    print(e)
    price, change, volume = [], [], []

  return price, change, volume


def scraping(stock_list, interupt_time, interval_time):#interupt and interval time are passed as seconds
  df = pd.DataFrame(columns=['Date','Code','Price','Change', '% Change', 'Volume'])

  start_time = time.time()
  current_time = time.time()

  while current_time - start_time < interupt_time:
    for stock_code in stock_list:
      time_stamp = datetime.datetime.now() - datetime.timedelta(hours=5)#converting our time to NY time
      time_stamp = time_stamp.strftime('%y-%m-%d %H:%M:%S')#format the time
      information: list = [time_stamp] 

      price, change, volume = real_time_price(stock_code)

      actual_change, percentage_change = str(change).split()
      percentage_change = percentage_change.replace('(', '')
      percentage_change = percentage_change.replace(')', '')
      #percentage_change = percentage_change.replace('%', '')

      information.extend([stock_code, price, actual_change, percentage_change, volume])
      df.loc[len(df)] = information#adds the information list to the datatframe
      time.sleep(interval_time)
      current_time = time.time()
  
  df.to_csv('StockData.csv',index=False)#saves all vales at once at the end of scraping

'''
#Running Stock Scraper
'''

Stock: list = ['NFLX']
scraping(Stock, 300, 10)