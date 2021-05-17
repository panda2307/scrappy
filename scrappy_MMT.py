import requests
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

today = datetime.datetime.today().strftime('%d/%m/%Y')
cities = ['BLR', 'DEL']

def GET_DATA(date, cities, num_clicks=15):
    
    '''
    extract data from the website. Returns a list with extracted details of prices.
    Inputs: date today; cities of travel (to and fro); number of clicks to make on the slider (default 15)
    Output type: list
    '''
    
    url = f'https://www.makemytrip.com/flight/search?tripType=O&itinerary={cities[0]}-{cities[1]}-{date}&paxType=A-1_C-0_I-0&cabinClass=E&sTime=1615833272958&forwardFlowRequired=true&mpo='
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)

    slider_text=[]
    for n in range(num_clicks):
        slider = driver.find_element_by_xpath('//*[@id="weeklyFare"]/div/div[2]/ul')
        slider_text += slider.text.split('\n')
        clickSlider = driver.find_element_by_xpath('//*[@id="weeklyFare"]/div/div[4]')
        clickSlider.click()

    driver.quit()
    return slider_text

def CLEAN_DATA(data, tag):
    
    '''
    Clean extracted data. Returns a DataFrame object. 
    Input type: list
    Output type: DataFrame
    '''
    
    dates_days=data[::2]
    prices_lst=data[1::2]
    prices_lst1=[pd.NaT if x == '--' else x for x in prices_lst]

    days = []
    dates = []
    for date in dates_days:
        dates.append(date.split(', ')[1])
        days.append(date.split(', ')[0])

    days = np.array(days).reshape(-1,1)
    dates = np.array(dates).reshape(-1,1)
    prices = np.array(prices_lst1).reshape(-1,1)

    val = np.concatenate((dates,days,prices), axis=1)
    info_df = pd.DataFrame(data=val, columns=['Date', 'Day', f'Price_({tag})'])
    info_df.dropna(inplace=True)
    info_df.loc[:, f'Price_({tag})']= [price.split('₹ ')[1].replace(',','') for price in info_df[f'Price_({tag})']]
    return info_df