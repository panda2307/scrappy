from bs4 import BeautifulSoup as BS
import requests
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import datetime
from util import click_nonStop, listings, info_df, update_info, datafetch

### USER DEFINED VARIABLES---------------------------------------------------
city_from = 'BLR'
city_to = 'DEL'
date_start = '08/04/2021'
date_end = '13/04/2021'
###--------------------------------------------------------------------------

url = f'https://www.makemytrip.com/flight/search?itinerary={city_from}-{city_to}-{date_start}_{city_to}-{city_from}-{date_end}&tripType=R&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng'

listing_left, listing_right = datafetch(url)

# n = int(input('Number of listings:'))
# Top 5 prices
n = 5
top_listingLeft = listing_left[:n]
top_listingRight = listing_right[:n]

current_info = info_df((top_listingLeft, top_listingRight), city_from, city_to)
current_info.insert(loc=0, column='Date Time', value=np.array(datetime.datetime.now().strftime('%d/%m/%y, %H:%M:%S')))

filename = f'{city_from}_{city_to}_Tickets_MMT.csv'

try:
    prev_info = pd.read_csv(filename)
except:
    current_info.to_csv(filename, index=False)
else:
    current_update = update_info(prev_info, current_info)
    current_update.to_csv(filename, index=False)