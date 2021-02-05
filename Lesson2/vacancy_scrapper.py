from bs4 import BeautifulSoup as bs
import requests as re
from pprint import pprint
import pandas as pn
'''Необходимо собрать информацию о вакансиях на вводимую должность 
(используем input или через аргументы) с сайтов Superjob и HH. Приложение должно анализировать несколько 
страниц сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
* Наименование вакансии.
* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
* Ссылку на саму вакансию.
* Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью 
dataFrame через pandas.'''



profession=input('Enter the profession name:\n')
url='https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text='+profession
# print(url)
list_of_vac=[]
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/83.0.4103.97 Safari/537.36'}

class WrongStatus(Exception):
    def __init__(self,text):
        self.text=text


with re.get(url,headers=headers) as data:
    try:
        if data.status_code!=200:
            raise WrongStatus
        bsdata=bs(data.text,'html.parser')
       # bsdata=bsdata.prettify(formatter=lambda s: s.replace(u'\xa0', ' '))
        for tags in bsdata.find_all('div',attrs={'class':'vacancy-serp-item__row vacancy-serp-item__row_header'}):
                vac_data = {}
                vacancy_block=tags.find('a',attrs={'class':'bloko-link HH-LinkModifier'})
                vac_data['vacancy']=vacancy_block.text
                salary_block=tags.find('span',attrs={'data-qa':'vacancy-serp__vacancy-compensation'})
                vac_data['link']=vacancy_block.get('href')
                if salary_block is not None:
                    vac_data['salary']=salary_block.text
                else:
                    continue
                list_of_vac.append(vac_data)
        pprint(list_of_vac)


    except WrongStatus:
        pprint("We didn't get data")

