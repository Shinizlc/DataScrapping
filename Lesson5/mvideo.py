from selenium import webdriver
from time import sleep
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
connection=MongoClient('127.0.0.1',27017)
db=connection['mvideo']
coll=db['HITS']
from pprint import pprint
driver = webdriver.Chrome('/Users/saleksei/Desktop/DataScapping/Lesson5/chromedriver')
driver.get('https://www.mvideo.ru/')
driver.maximize_window()
try:
    data_to_mongo={}
    
    next_button=driver.find_element_by_css_selector('.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')
    for i in range(0,6):
        next_button.click()
        sleep(3)
    sale_hits=driver.find_element_by_xpath("//*[contains(text(),'Хиты продаж')]/../../..")
    for hit in sale_hits.find_elements_by_class_name('gallery-list-item'):
        data_to_mongo['title'] = hit.find_element_by_css_selector('.fl-product-tile-title__link.sel-product-tile-title').get_attribute('title')
        data_to_mongo['price_hits']=sale_hits.find_element_by_class_name('fl-product-tile-price__current')
        pprint(data_to_mongo)
except ElementClickInterceptedException:
    sleep(3)
    next_button = driver.find_element_by_css_selector('.next-btn.c-btn.c-btn_scroll-horizontal.c-btn_icon.i-icon-fl-arrow-right')
    next_button.click()


driver.close()