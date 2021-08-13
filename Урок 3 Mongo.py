#Домашнее задание
#Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные вакансии в созданную БД.
#Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
#Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.


#https://stavropol.hh.ru/search/vacancy?clusters=true&area=113&ored_clusters=true&enable_snippets=true&st=searchVacancy&text=Data&page=
# https://russia.superjob.ru/vacancy/search/?keywords=Data
from bs4 import BeautifulSoup as bs
import requests
import re
from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'basar'
DATASET_PATH = 'F:/Lesson/файлы/result.csv'
client = MongoClient(MONGO_URI)
mongo_base = client[MONGO_DATABASE]

collection = mongo_base['vacancy']

vacancy_list_hh = []
page = 0
while True:

    main_link_hh = 'https://stavropol.hh.ru'
    params = {'L_is_autosearch': 'false',
              'clusters': 'true',
              'area': 113,
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'st' : 'searchVacancy',
              'text': 'Data',
              'page': {page}
              }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    html = requests.get(main_link_hh + '/search/vacancy', params=params, headers=headers)

    soup = bs(html.text, 'html.parser')

    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.find_all('div', {'class': 'vacancy-serp-item'})

    p = soup.find('div', {'data-qa': 'pager-block'}).text

    p = (re.search(r'дальше', p))
# подготовка данных для записи
    for i in vacancies_list:
        vacancy_name = i.find('a').text
        vacancy_info = i.find('a')['href']
        vacancy_info_z1 = i.find('div', {'class':"vacancy-serp-item__sidebar"}).getText()
        vacancy_info_z = [vacancy_info_z1.replace('\u202f', '')]
        #print(vacancy_info_z)
        match1=[]
        if vacancy_info_z[0] != '':
            for a in re.split(r'-', vacancy_info_z[0]):
                m = [el for el in re.findall(r'\d+', a)]
                match1.append(m[0])
            currency = vacancy_info_z1.split()[-1]
        else:
            currency = ''
        min_c = 'По договорённости'
        max_c = 'По договорённости'
        if vacancy_info_z1.startswith('от'):
            min_c = int(match1[0])
            max_c = 'По договорённости'
        elif vacancy_info_z1.startswith('до'):
            min_c = 'По договорённости'
            max_c = int(match1[0])
        elif ('-') in vacancy_info_z1:
            min_c = int(match1[0])
            max_c = int(match1[1])
# Заполнение словаря и списка вакансий запись и обновление базы (задание 2)
        vacancy_dict = {}
        vacancy_dict['name'] = vacancy_name
        vacancy_dict['link'] = vacancy_info
        vacancy_dict['min'] = min_c
        vacancy_dict['max'] = max_c
        vacancy_dict['currency'] = currency
        vacancy_dict['website'] = 'hh.ru'
        collection.update_one({'link': vacancy_info}, {'$set': vacancy_dict}, upsert=True)
        #pprint(vacancy_dict)

    if p != None and p[0] == 'дальше':
        page += 1
        #print(page, end='\r')

    else:
        break

page = 1
while True:

    main_link_sj = 'https://superjob.ru'
    params = {'keywords': 'Data',
              'noGeo': 1,
              'page': {page}
              }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    html = requests.get(main_link_sj + '/vacancy/search/', params=params, headers=headers)

    soup = bs(html.text, 'html.parser')

    vacancies_block = soup.find('div', {'class': '_1Ttd8 _2CsQi'})

    vacancies_list = vacancies_block.find_all('div', {'class': 'jNMYr GPKTZ _1tH7S'})

    p = soup.find('div', {'_3zucV L1p51 _3ZDWc _2LZO7 iBQ9h GpoAF _3fOgw'}).text

    for i in vacancies_list:
        #pprint(i)
        vacancy_info = (main_link_sj + i.find('a')['href'])
        #print(vacancy_info)
        vacancy_name = i.find('a').text
        #print(vacancy_name)


        vacancy_info_z1 = i.find('span', {'class':'_1OuF_ _1qw9T f-test-text-company-item-salary'}).getText()
        #print(vacancy_info_z1)
        min_c = ''
        max_c = ''
        currency = ''
        match1=[]
# Подготовка цифр для записи
        if vacancy_info_z1 != 'По договорённости':
            currency = vacancy_info_z1.split()[-1]
            vacancy_info_z = [vacancy_info_z1.replace('\xa0', '')]
            for a in re.split(r'—', vacancy_info_z[0]):
                m = [el for el in re.findall(r'\d+', a)]
                match1.append(m[0])
                #print(match1)
        else:
            min_c = vacancy_info_z1
            max_c = vacancy_info_z1
        if vacancy_info_z1.startswith('от'):
            min_c = int(match1[0])
            max_c = 'По договорённости'
        elif vacancy_info_z1.startswith('до'):
            min_c = 'По договорённости'
            max_c = int(match1[0])
        elif ('—') in vacancy_info_z1:
            min_c = int(match1[0])
            max_c = int(match1[1])
# Заполнение словаря и списка вакансий запись и обновление базы (задание 3)
        vacancy_dict = {}
        vacancy_dict['name'] = vacancy_name
        vacancy_dict['link'] = vacancy_info
        vacancy_dict['min'] = min_c
        vacancy_dict['max'] = max_c
        vacancy_dict['currency'] = currency
        vacancy_dict['website'] = 'superjob.ru'
        collection.update_one({'link': vacancy_info}, {'$set': vacancy_dict}, upsert=True )
        #pprint(vacancy_dict)

    if (re.findall(r'\w\w\w\w\w\w$', p)[0]) == 'Дальше':
        page += 1
    else:
        break
#Введение суммы минимальной зарплаты для отсеивания вакансий (задание 2)
sum_min = int(input("input min sum: "))
a = collection.find({"$or":
                         [{'min': {'$nin': "По договоренности"}, 'min': {'$gt': sum_min}},
                          {'max': {'$nin': "По договоренности"}, 'max': {'$gt': sum_min}}]})
#print(list(a))
for i in a:
    print(i)