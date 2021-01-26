'''1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
 для конкретного пользователя, сохранить JSON-вывод в файле *.json.'''
import requests as re
def get_repos_names():
    user_name='TheAlgorithms'#input('Enter the name of the user:\n')
    url=f"https://api.github.com/users/{user_name}/repos"
    with re.get(url) as link:
        for i in link.json():
            print(i['name'])

if __name__=='__main__':
    get_repos_names()