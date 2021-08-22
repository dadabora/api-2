# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy

    def process_item(self, item, spider):
        # Здесь обработка item'a

        if spider.name == 'hhru':
            min_c = 'По договорённости'
            max_c = 'По договорённости'
            currency = ''
            vacancy_info_z = []
            for _ in item['salary']:
                s = _.replace("\xa0", "")
                vacancy_info_z.append(s)
                # print(vacancy_info_z)
            item['salary'] = vacancy_info_z[0]
            #обработка зарплаты
            match1 = []
            if vacancy_info_z[0] != 'з/п не указана':
                for a in re.split(r'-', vacancy_info_z[0]):
                    m = [el for el in re.findall(r'\d+', a)]
                    match1 = m
                currency = vacancy_info_z[0].split()[-1]
                # print(vacancy_info_z[0])
                if re.fullmatch(r'от.* до.*', vacancy_info_z[0]):
                    min_c = int(match1[0])
                    max_c = int(match1[1])
                elif ('от') in vacancy_info_z[0]:
                    min_c = int(match1[0])
                    max_c = 'По договорённости'
                elif ('до') in vacancy_info_z[0]:
                    min_c = 'По договорённости'
                    max_c = int(match1[0])
            item['min'] = min_c
            item['max'] = max_c
            item['currency'] = currency
            item['website'] = 'hh.ru'
        elif spider.name == 'sjru':
            pass

        collection = self.mongobase[spider.name]
       # collection.insert_one(item)
        collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        return item
