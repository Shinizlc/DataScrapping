from selenium import webdriver
from time import sleep
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
connection=MongoClient('127.0.0.1',27019)
db=connection['mvideo']
coll=db['HITS']
from pprint import pprint
driver = webdriver.Chrome('/Users/saleksei/Desktop/DataScapping/Lesson5/chromedriver')
driver.get('https://www.mvideo.ru/')
driver.maximize_window()
try:
    list_of_data=[]
    for i in range(0,3):
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right'))).click()  # doesn't resolve the error ElementClickInterceptedException
        sleep(3)
        sale_hits=driver.find_element_by_xpath("//*[contains(text(),'Хиты продаж')]/../../..")
        for hit in sale_hits.find_elements_by_class_name('gallery-list-item')[:5]:
            data_to_mongo = {}
            data_to_mongo['title'] = hit.find_element_by_css_selector('.fl-product-tile-title__link.sel-product-tile-title').get_attribute('title')
            data_to_mongo['price_hits'] = hit.find_element_by_class_name('fl-product-tile-price__current').text
            if len(list_of_data)>0:
                if data_to_mongo in list_of_data:
                    continue
                else:
                    list_of_data.append(data_to_mongo)

            else:
                list_of_data.append(data_to_mongo)



    pprint(list_of_data)
    coll.insert_many(list_of_data)
except ElementClickInterceptedException:
    sleep(3)
    next_button = driver.find_element_by_css_selector('.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')
    next_button.click()


driver.close()