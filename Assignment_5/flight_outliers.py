
# coding: utf-8

import time
import re
from unidecode import unidecode
import pandas as pd
import datetime
from dateutil.parser import parse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# ======== Task 1 =========
def scrape_data(start_date, from_place, to_place, city_name):
    """
    start_date: a datetime object for the start date that you should use in your query to Google Flight explorer
    from_place: a string with the name of the origin of the flights
    to_place: a string with the name of the regional destination of the flights
    city_name: a string for the name of the city who's data that you should actually scrape
    
    return: a pandas DataFrame object with two columns "Date_of_Flight" and "Price." , and one row for each day, totally 60 rows
    
    """
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    time.sleep(2)  # wait for the driver to load data
    
    # from_place
    driver.find_elements_by_class_name('LJTSM3-p-a')[0].click()
    ActionChains(driver).send_keys(from_place).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    
    # to_place
    driver.find_elements_by_class_name('LJTSM3-p-a')[1].click()
    ActionChains(driver).send_keys(to_place).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    
    # start_date
    start_date_str = start_date.strftime("%Y-%m-%d")
    url_date = driver.current_url[:-10] + start_date_str
    driver.get(url_date)
    time.sleep(2)
    
    # use city_name to choose target city
    results_city = driver.find_elements_by_class_name('LJTSM3-v-c')
    city_num = None

    for i in range(len(results_city)):
        city = results_city[i]
        if re.findall(city_name.lower(), unidecode(city.text).lower()):
            city_num = i
    if city_num == None:
        raise Exception('City Name not Found!')    
    time.sleep(2)
    
    # get bars of target city
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    target = results[city_num]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    data = []
    time.sleep(2)

    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.01)
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,  # get price
               target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))      # get date of flight

    data = [x for x in data if str(x[0]) != '']  # exclude null bars
    
    # convert into dataframe and return
    clean_data = [(float(d[0].replace('$', '').replace(',', '')), parse(d[1].split('-')[0].strip()))  for d in data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Date_of_Flight'])
    driver.quit()
    return df 

# Test
from_place = 'Beijing'
to_place = 'Mexico'
start_date = datetime.datetime(2017, 04, 10)
city_name = 'Cancun'

data_60 = scrape_data(start_date, from_place, to_place, city_name)
print data_60



# ======== Task 2 =========
def scrape_data_90(start_date, from_place, to_place, city_name):
    """
    start_date: a datetime object for the start date that you should use in your query to Google Flight explorer
    from_place: a string with the name of the origin of the flights
    to_place: a string with the name of the regional destination of the flights
    city_name: a string for the name of the city who's data that you should actually scrape
    
    return: a pandas DataFrame object with 90 rows and 2 columns "Date_of_Flight" and "Price"
    
    """
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/flights/explore/')
    time.sleep(2)  # wait for the driver to load data
    
    # from_place
    driver.find_elements_by_class_name('LJTSM3-p-a')[0].click()
    ActionChains(driver).send_keys(from_place).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    
    # to_place
    driver.find_elements_by_class_name('LJTSM3-p-a')[1].click()
    ActionChains(driver).send_keys(to_place).perform()
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    
    # start_date
    start_date_str = start_date.strftime("%Y-%m-%d")
    url_date = driver.current_url[:-10] + start_date_str
    driver.get(url_date)
    time.sleep(2)
    
    # use city_name to choose target city
    results_city = driver.find_elements_by_class_name('LJTSM3-v-c')
    city_num = None

    for i in range(len(results_city)):
        city = results_city[i]
        if re.findall(city_name.lower(), unidecode(city.text).lower()):
            city_num = i
    if city_num == None:
        raise Exception('City Name not Found!')    
    time.sleep(2)
    
    # get bars of target city
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    target = results[city_num]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    data = []
    time.sleep(2)

    for bar in bars:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.01)
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,  # get price
               target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))      # get date of flight

    data = [x for x in data if str(x[0]) != '']  # exclude null bars
    
    # select the next 30 days
    driver.find_elements_by_class_name('LJTSM3-w-D')[1].click()  # the first one is 30 days from start_date
    time.sleep(2)    
    
    # find target city again (the order may change after clicking)
    results_city = driver.find_elements_by_class_name('LJTSM3-v-c')
    city_num = None

    for i in range(len(results_city)):
        city = results_city[i]
        if re.findall(city_name.lower(), unidecode(city.text).lower()):
            city_num = i
    if city_num == None:
            raise Exception('There is no flight to this city after 60 days!')
    time.sleep(1)
    
    # append the rest data (90 days in total)
    results = driver.find_elements_by_class_name('LJTSM3-v-d')
    target = results[city_num]
    bars = target.find_elements_by_class_name('LJTSM3-w-x')
    time.sleep(2)

    for bar in bars[30:60]:
        ActionChains(driver).move_to_element(bar).perform()
        time.sleep(0.01)
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,  #get price
               target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))  #get time period
    
    data = [x for x in data if str(x[0]) != '']  # to exclude null bars
        
    # convert into dataframe and return
    clean_data = [(float(d[0].replace('$', '').replace(',', '')), parse(d[1].split('-')[0].strip()))  for d in data]   
    df = pd.DataFrame(clean_data, columns=['Price', 'Date_of_Flight'])
    driver.quit()
    return df 

# Test
from_place = 'Beijing'
to_place = 'America'
start_date = datetime.datetime(2017, 04, 10)
city_name = 'Boston'

data_90 = scrape_data_90(start_date, from_place, to_place, city_name)
print data_90

2+2