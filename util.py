from selenium import webdriver
from tqdm import tqdm
import time
import pandas as pd
import numpy as np

# Helper Functions (Can be directly integrated as methods inside driver object as a next step):

def click_nonStop(driver):
    '''
    Function to click the 'Non Stop' option in MMT Website. Hard coded to the exact X-Path location of the element.
    '''
#     Ob1 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/div/div[1]/div/div[2]/div/div[1]/div/label[1]/div/span[1]/span')
    Ob1 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/label[1]/div/span[1]')
#     Ob2 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/div/div[1]/div/div[3]/div/div[1]/div/label[1]/div/span[1]/span')
    Ob2 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div/div[3]/div/div[1]/div/label[1]/div/span[1]')
    Ob1.click()
    Ob2.click()

def listings(driver):
    '''
    Function to fetch all the required data from the listings. Left and Right denote the to and fro ticket prices and times.
    '''
    listing_left = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div/div/div[1]/div[2]')
    listing_right = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[3]/div/div[2]/div/div/div/div[2]/div[2]')

    listing_left_list = listing_left.find_elements_by_class_name('splitViewListing')
    listing_right_list = listing_right.find_elements_by_class_name('splitViewListing')
    
    for i, el in enumerate(listing_left_list):
        listing_left_list[i] = el.text
    for i, el in enumerate(listing_right_list):
        listing_right_list[i] = el.text
    
    return listing_left_list, listing_right_list

def merge_dicts(dict_list):
    '''
    Merges a list of dictionaries with same keys
    '''
    output = dict.fromkeys(dict_list[0],[])
    for key in output.keys():
        output[key] = [d[key] for d in dict_list]
    return output

def info_df(listing_info, city_from, city_to):
    '''
    Appending data to readable pandas dataframe, making suitable to save in CSV format more easily.
    '''
    Left_info = []
    Right_info = []
    top_listingLeft, top_listingRight = listing_info
    ruppee_symbol = '₹'
    for el_left, el_right in zip(top_listingLeft, top_listingRight):

        timings_left = el_left.split(ruppee_symbol)[0].strip().split('\n')
        cost_left = int(el_left.split(ruppee_symbol)[1].strip().replace(',',''))
        Left_info.append([timings_left[0], timings_left[1], timings_left[3], timings_left[5], cost_left])

        timings_right = el_right.split(ruppee_symbol)[0].strip().split('\n')
        cost_right = int(el_right.split(ruppee_symbol)[1].strip().replace(',',''))
        Right_info.append([timings_right[0], timings_right[1], timings_right[3], timings_right[5], cost_right])
        
    Info = np.concatenate((np.array(Left_info), np.array(Right_info)), axis=1)
    header = [f'Airline ({city_from})', f'Departure ({city_from})', f'Duration ({city_from})', f'Arrival ({city_from})', f'Cost ({city_from})',
              f'Airline ({city_to})', f'Departure ({city_to})', f'Duration ({city_to})', f'Arrival ({city_to})', f'Cost ({city_to})']

    df = pd.DataFrame(data=Info, columns=header)
    return df

def update_info(prev_info, current_info):
    '''
    Update the previous listing information with the current batch of data.
    '''
    current_update = prev_info.append(current_info)
    return current_update

def datafetch(url):
    '''
    Main function to send requests to the website and get pricing and timing information of airlines.
    '''
    start = time.time()
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    
    click_nonStop(driver)
    listing_left, listing_right = listings(driver)
    driver.quit()
    print('Time Elapsed in Fetching from site: ', time.time()-start)
    
    return listing_left, listing_right