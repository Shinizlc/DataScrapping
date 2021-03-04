from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pymongo import MongoClient
import re
from pprint import pprint
#db_conn=MongoClient('127.0.0.1',27017)
browser=webdriver.Chrome('/Users/saleksei/Desktop/DataScapping/Lesson5/chromedriver')
browser.maximize_window()

browser.get('https://mail.ru/')
email=browser.find_element_by_name('login')
email.send_keys('study.ai_172')
domain=browser.find_element_by_name('domain')
select_domain=Select(domain)
select_domain.select_by_value('@mail.ru')
email.send_keys(Keys.ENTER)
browser.implicitly_wait(10)
password=browser.find_element_by_name('password')
password.send_keys('NextPassword172')
password.send_keys(Keys.ENTER)

# mail_elem=browser.find_element_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
# while True:
#     mail_elem.send_keys(Keys.PAGE_DOWN)
#     browser.implicitly_wait(1)


# mail_elem=browser.find_elements_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
# pprint(mail_elem)
# for mail in mail_elem:
#     sleep(5)
#     mail_from=mail.find_element_by_class_name('ll-crpt').get_attribute('title')
#     mail_title=mail.find_element_by_class_name('ll-sj__normal').text
#     pprint(f'the letter from {mail_from} has the following title:{mail_title}')
#     enter_the_mail=mail.click()
#     # text_block=browser.find_element_by_class_name('mcnTextBlockInner_mr_css_attr')
#     # data=text_block.find_elements_by_tag_name('p').text
#     return_button=WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button2.button2_has-ico.button2_arrow-back.button2_pure.button2_ico-text-top.button2_nowrap.button2_hover-support.js-shortcut')))
#     return_button.click()


#browser.close()
# i=0
# while i<5:
#
#     sleep(2)
#     mail_elem=browser.find_elements_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
#     mail_from=mail_elem[i].find_element_by_class_name('ll-crpt').get_attribute('title')
#     mail_title=mail_elem[i].find_element_by_class_name('ll-sj__normal').text
#     pprint(f'the letter from {mail_from} has the following title:{mail_title}')
#     enter_the_mail=mail_elem[i].click()
#     # text_block=browser.find_element_by_class_name('mcnTextBlockInner_mr_css_attr')
#     # data=text_block.find_elements_by_tag_name('p').text
#     return_button=WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button2.button2_has-ico.button2_arrow-back.button2_pure.button2_ico-text-top.button2_nowrap.button2_hover-support.js-shortcut')))
#     return_button.click()
#     i += 1


# num_mail=0
# while True:
#     mail_list=browser.find_elements_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')
#     pprint(len(mail_list))
#     if len(mail_list)>num_mail:
#         actions=ActionChains(browser)
#         actions.move_to_element(mail_list[-1])
#         actions.perform()
#         num_mail=len(mail_list)
#     else:
#         break
list_to_mongo=[]

c=0
while c<20:
    mail_list = browser.find_elements_by_css_selector('.llc.js-tooltip-direction_letter-bottom.js-letter-list-item.llc_normal')#после первой итерации и смещения поиск возвращает 0 новых объектов
    #pprint(len(mail_list))
    actions=ActionChains(browser)
    actions.move_to_element(mail_list[-1])#получаю ошибку на второй же итерации
    actions.perform()
    c += 1
    #pprint(len(mail_list))
    for mails in mail_list[:2]:#ограничил временно
        d = {}
        d['mail_from'] = mails.find_element_by_class_name('ll-crpt').get_attribute('title')
        d['mail_title'] = mails.find_element_by_class_name('ll-sj__normal').text
        d['mail_href'] = mails.get_attribute('href')
        d['mail_date'] = mails.find_element_by_css_selector('.llc__item.llc__item_date').get_attribute('title')
        list_to_mongo.append(d)
    pprint(list_to_mongo)
    for get_text in list_to_mongo[:2]: #ограничил временно
        browser.get(get_text.get('mail_href'))
        email_body=browser.find_element_by_class_name('letter-body').text
        get_text['full_text']=email_body
        return_button=WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button2.button2_has-ico.button2_arrow-back.button2_pure.button2_ico-text-top.button2_nowrap.button2_hover-support.js-shortcut')))
        return_button.click()
    pprint(list_to_mongo)

browser.close()
