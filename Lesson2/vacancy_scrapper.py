from bs4 import BeautifulSoup as bs
import requests as req
from pprint import pprint
import re
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


pages=int(input('Enter the number of pages:\n'))
profession=input('Enter the profession name:\n')
website='hh.ru'
url='https://spb.hh.ru/search/vacancy?area=2&fromSearchLine=true&st=searchVacancy&text='+profession

list_of_vac=[]
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/83.0.4103.97 Safari/537.36'}

class WrongStatus(Exception):
    def __init__(self,text):
        self.text=text


class EndScrapping(Exception):
    def __init__(self,text):
        self.text=text
while True:
    with req.get(url, headers=headers) as data:
        try:
            if data.status_code != 200:
                raise WrongStatus
            bsdata = bs(data.text, 'html.parser')
            for tags in bsdata.find_all('div', attrs={'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'}):
                vac_data = {}
                vacancy_block = tags.find('a', attrs={'class': 'bloko-link HH-LinkModifier'})
                vac_data['vacancy'] = vacancy_block.text
                salary_block = tags.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                vac_data['link'] = vacancy_block.get('href')
                vac_data['website'] = website
                if salary_block is not None:
                    salary = salary_block.text
                    salary = re.sub(r'\xa0', '', salary)
                    if re.search(r'^от ([0-9]+)', salary):
                        vac_data['max_salary'] = None
                        vac_data['min_salary'] = re.findall(r'^от ([0-9]+)', salary)
                        vac_data['currency'] = re.findall(r'^от [0-9]+ (\w+).', salary)
                    elif re.search(r'^до ([0-9]+)', salary):
                        vac_data['max_salary'] = re.findall(r'^до ([0-9]+)', salary)
                        vac_data['min_salary'] = None
                        vac_data['currency'] = re.findall(r'^до [0-9]+ (\w+).', salary)
                    else:
                        vac_data['max_salary'] = re.findall(r'\d+-(\d+)', salary)
                        vac_data['min_salary'] = re.findall(r'(\d+)-\d+', salary)
                        vac_data['currency'] = re.findall(r'\d+-\d+ (\w+).', salary)



                else:
                    vac_data['min_salary'] = None
                    vac_data['max_salary'] = None
                    vac_data['currency'] = None
                list_of_vac.append(vac_data)
            #pprint(list_of_vac)


            for pag in bsdata.find_all('a',{'data-qa':'pager-next'}):
                if int(pag.get('data-page')) < pages:
                    pprint(int(pag.get('data-page')))
                    pprint(pages)
                    url='https://spb.hh.ru'+pag.get('href')
                    pprint(url)
                else:
                    raise EndScrapping('text')

        except WrongStatus:
            pprint("We didn't get data")
        except EndScrapping:
            break

