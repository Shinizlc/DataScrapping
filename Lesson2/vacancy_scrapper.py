from bs4 import BeautifulSoup as bs
import requests as re
from pprint import pprint
# import pandas as pn
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


#pages=int(input('Enter the number of pages:\n'))
profession=input('Enter the profession name:\n')
list_of_pages=['https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text='+profession]
website='hh.ru'
url='https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text='+profession

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

#####не разобрался, вроде настроил поиск блоков, где находятся ссылки на страницы правильно,
#####но почему вытаскивает неправильные ссылки. Что может быть не так?
        # all_pages=bsdata.find_all('a',{'data-qa':'pager-page'})
        # for pag in all_pages:
        #     if int(pag.get('data-page'))<=pages:
        #         list_of_pages.append('https://spb.hh.ru/'+pag.get('href'))
        #     else:
        #         continue
        # pprint(list_of_pages)

        for tags in bsdata.find_all('div',attrs={'class':'vacancy-serp-item__row vacancy-serp-item__row_header'}):
                vac_data = {}
                vacancy_block=tags.find('a',attrs={'class':'bloko-link HH-LinkModifier'})
                vac_data['vacancy']=vacancy_block.text
                salary_block=tags.find('span',attrs={'data-qa':'vacancy-serp__vacancy-compensation'})
                vac_data['link']=vacancy_block.get('href')
                vac_data['website']=website
                if salary_block is not None:
                    #не понял как работать с таким форматированием 40\xa0000-60\xa0000 руб
                    vac_data['salary']=salary_block.text
                else:
                    continue
                list_of_vac.append(vac_data)
        pprint(list_of_vac)


    except WrongStatus:
        pprint("We didn't get data")

