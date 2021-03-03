from selenium import webdriver
from time import sleep
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
connection=MongoClient('127.0.0.1',27017)
db=connection['mvideo']
coll=db['HITS']
from pprint import pprint
driver = webdriver.Chrome('/Users/saleksei/Desktop/DataScapping/Lesson5/chromedriver')
driver.get('https://www.mvideo.ru/')
driver.maximize_window()
try:
    list_of_data=[]
    data_to_mongo={}
    #next_button=driver.find_element_by_css_selector('.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')
    for i in range(0,6):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right'))).click()  # doesn't resolve the error ElementClickInterceptedException
        sleep(3)
    sale_hits=driver.find_element_by_xpath("//*[contains(text(),'Хиты продаж')]/../../..")
    for hit in sale_hits.find_elements_by_class_name('gallery-list-item'):
        data_to_mongo['title'] = hit.find_element_by_css_selector('.fl-product-tile-title__link.sel-product-tile-title').get_attribute('title')
        data_to_mongo['price_hits'] = hit.find_element_by_class_name('fl-product-tile-price__current').text
        #pprint(data_to_mongo)
        list_of_data.append(data_to_mongo)
    pprint(list_of_data)
    #coll.insert_many(list_of_data)
except ElementClickInterceptedException:
    sleep(3)
    next_button = driver.find_element_by_css_selector('.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')
    next_button.click()


driver.close()