
# coding: utf-8

import time
import re
import pandas as pd
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
from dateutil.parser import parse
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.spatial import distance


# ======== Task 1 =========
def scrape_data(start_date, from_place, to_place, city_name):
    """
    start_date: a datetime object for the start date that you should use in your query to Google Flight explorer
    from_place: a string with the name of the origin of the flights
    to_place: a string with the name of the regional destination of the flights
    city_name: a string for the name of the city who's data that you should actually scrape
    
    return: a pandas DataFrame object with two columns "Date_of_Flight" & "Price", one row for each day(totally 60 rows)
    
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
    if city_num is None:
        driver.quit()
        raise Exception('City Name Not Found!')    
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
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,  # price
               target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))   # date of flight

    data = [x for x in data if str(x[0]) != '']  # exclude null bars
    
    # convert into DataFrame and return
    clean_data = [(float(d[0].replace('$', '').replace(',', '')), parse(d[1].split('-')[0].strip())) for d in data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Date_of_Flight'])
    driver.quit()
    return df 

# Test for task 1
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Mexico City')
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Cancun')
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'United States', 'San Francisco')
# print data_60


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
    if city_num is None:
        driver.quit()
        raise Exception('City Name Not Found!')    
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
        data.append((target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[0].text,  # price
               target.find_element_by_class_name('LJTSM3-w-k').find_elements_by_tag_name('div')[1].text))   # date of flight

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
    if city_num is None:
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
        
    # convert into DataFrame and return
    clean_data = [(float(d[0].replace('$', '').replace(',', '')), parse(d[1].split('-')[0].strip())) for d in data]
    df = pd.DataFrame(clean_data, columns=['Price', 'Date_of_Flight'])
    driver.quit()
    return df 

# Test for task 2
# data_90 = scrape_data_90(datetime.datetime(2017, 4, 15), 'Beijing', 'America', 'Boston')
# data_90 = scrape_data_90(datetime.datetime(2017, 4, 15), 'Beijing', 'United States', 'San Francisco')
# print data_90


# ========== Task 3 question 1 ==========
def task_3_dbscan(flight_data):
    """
    flight_data:a pandas DataFrame object with 2 columns 'Price' & 'Date_of_Flight', one row for each day
    return:a pandas DataFrame object with 2 columns 'Price' & 'Date_of_Flight',  one row for each outlier flight
    """
    df = flight_data
    start_date = []
    for i in range(len(df)):
        start_date.append((df['Date_of_Flight'][i] - df['Date_of_Flight'][0]).days + 1)
    
    # clustering
    df['Start_Date'] = pd.Series(start_date).values
    X = StandardScaler().fit_transform(df[['Start_Date', 'Price']])
    db = DBSCAN(eps=0.3, min_samples=3).fit(X)
    df['dbscan_labels'] = db.labels_
    
    # plot results of clustering
    labels = db.labels_
    clusters = len(set(labels))
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    matplotlib.style.use('ggplot')
    plt.subplots(figsize=(12, 8))
    
    for k, c in zip(unique_labels, colors):
        class_member_mask = (labels == k)  # get all the points in class k
        xy = X[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=c, markeredgecolor='k', markersize=14)
 
    plt.title("Total Clusters: {}".format(clusters) + " Eps=0.3 Min_spl=3", fontsize=14, y=1.01)
    plt.savefig('task_3_dbscan.png')
    
    # Mean of each cluster & other features of cluster
    mean_points = []
    for n in unique_labels:
        x = pd.DataFrame(X)[df.dbscan_labels == n]
        mp = x.mean(axis=0)
        # calculate threshold for each cluster
        d = df[df.dbscan_labels == n]
        m = np.mean(d.Price)
        std = np.std(d.Price)
        thrshd = m - max(2*std, 50)
        mean_points.append((n, mp[0], mp[1], m, std, thrshd))
    
    mean_points = pd.DataFrame(mean_points)
    mean_points.columns = ['Cluster', 'Start_Date_X', 'Price_X', 'Mean_Price', 'Std_Price', 'Threshold']
    mean_points = mean_points[mean_points.Cluster != -1]
    
    # Outliers with scaled features
    df_outliers = pd.DataFrame(X)[df.dbscan_labels == -1]
    df_outliers.columns = ['Start_Date_X', 'Price_X']
    
    # Find the closest cluster for outlier flights
    # min_dist_list = []
    nearest_cluster = []
    for j in range(df_outliers.shape[0]):
        outlier = df_outliers.iloc[j]
        dist = []
        for i in range(mean_points.shape[0]):
            mean = mean_points[['Start_Date_X', 'Price_X']].iloc[i]
            dist.append(distance.euclidean(outlier, mean))
        # min_dist_list.append(min(dist))
        for k, d in enumerate(dist):
            if d == min(dist):
                nearest_cluster.append(k)
    
    outliers = df_outliers.copy()
    outliers['closest_cluster'] = pd.Series(nearest_cluster).values  # Nearest cluster of each outlier
    outliers['Price'] = df['Price'][df.dbscan_labels == -1]  # Original price of each outlier
    outliers['Date_of_Flight'] = df['Date_of_Flight'][df.dbscan_labels == -1]  # Original date of each outlier
    outliers['threshold'] = mean_points['Threshold'][outliers['closest_cluster']].values  # Threshold of the closest cluster
    
    result = outliers[['Price', 'Date_of_Flight']][outliers.Price <= outliers.threshold]
    if result.shape[0] != 0:
        return result
    else:
        raise Exception('There is no outlier price in this period!')  
    

# Test for task 3 question 1
data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Mexico City')
print data_60
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Cancun')
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'United States', 'San Francisco')
outliers_dbscan = task_3_dbscan(data_60)
print outliers_dbscan


# ======== Task 3 question 2 =========
def task_3_IQR(flight_data):
    """
    flight_data:a pandas DataFrame object with 2 columns 'Price' & 'Date_of_Flight', one row for each day
    return:a pandas DataFrame object with 2 columns 'Price' & 'Date_of_Flight',  one row for each outlier flight
    """
    plt.boxplot(flight_data['Price'])
    plt.title('Boxplot of Prices')
    plt.savefig('task_3_iqr.png')
    
    q1 = np.percentile(flight_data['Price'], 25)
    q3 = np.percentile(flight_data['Price'], 75)
    IQR = q3 - q1
    low_bound = q1-1.5*IQR
    outliers = flight_data[flight_data['Price'] < low_bound]
    if outliers.shape[0] != 0:
        return outliers
    else:
        raise Exception('There is no outlier price!')

# Test for task 3 question 2
data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Mexico City')
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'Mexico', 'Cancun')
# data_60 = scrape_data(datetime.datetime(2017, 4, 15), 'Beijing', 'United States', 'San Francisco')
outliers_IQR = task_3_IQR(data_60)
print outliers_IQR
