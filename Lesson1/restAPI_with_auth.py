'''Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.'''
import json
import requests
import os
def get_film_info():
    film=input('Enter the name of the film:\n')
    url='http://www.omdbapi.com/?'
    file_loc=os.path.dirname(__file__)
    file_name=file_loc+'/'+film+'.json'
    print(file_name)
    #headers={'X-API-Key':'b066c3e3'}
    paramters={'apikey':'b066c3e3','t':film}
    with requests.get(url,params=paramters) as endpoint:
        json_data=endpoint.json()
        #print(f"The duration of the {film} is {json_data.get('Runtime')}.The genre is {json_data.get('Genre')} and has a rating {json_data.get('Rated')}")
        with open(file_name,'w') as film_info:
            json.dump(json_data,film_info)


if __name__=='__main__':
    get_film_info()